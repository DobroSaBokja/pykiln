const vscode = require('vscode');

function getTagInfoAtPosition(document, position) {
    const line = document.lineAt(position.line).text;
    const char = position.character;

    let start = char;
    while (start > 0 && /[a-zA-Z0-9_:-]/.test(line[start - 1])) start--;
    let end = char;
    while (end < line.length && /[a-zA-Z0-9_:-]/.test(line[end])) end++;

    if (start === end) return null;

    const before = line.substring(0, end);
    const isCloseTag = /.*<\/[a-zA-Z0-9_:-]+$/.test(before);
    const isOpenTag = !isCloseTag && /.*<[a-zA-Z0-9_:-]+$/.test(before);

    if (!isOpenTag && !isCloseTag) return null;

    return {
        tagName: line.substring(start, end),
        range: new vscode.Range(position.line, start, position.line, end),
        isClose: isCloseTag
    };
}

function findMatchingCloseTagRange(document, tagName, afterOffset) {
    const text = document.getText();
    const escaped = tagName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const openRe = new RegExp(`<${escaped}[\\s>/]`, 'g');
    const closeRe = new RegExp(`</${escaped}[\\s>]`, 'g');

    const events = [];
    let m;

    openRe.lastIndex = afterOffset;
    while ((m = openRe.exec(text)) !== null) events.push({ type: 'open', index: m.index });

    closeRe.lastIndex = afterOffset;
    while ((m = closeRe.exec(text)) !== null) events.push({ type: 'close', index: m.index });

    events.sort((a, b) => a.index - b.index);

    let depth = 1;
    for (const ev of events) {
        if (ev.type === 'open') {
            depth++;
        } else {
            depth--;
            if (depth === 0) {
                const nameStart = ev.index + 2; // skip </
                return new vscode.Range(
                    document.positionAt(nameStart),
                    document.positionAt(nameStart + tagName.length)
                );
            }
        }
    }
    return null;
}

function findMatchingOpenTagRange(document, tagName, beforeOffset) {
    const text = document.getText().substring(0, beforeOffset);
    const escaped = tagName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const openRe = new RegExp(`<${escaped}[\\s>/]`, 'g');
    const closeRe = new RegExp(`</${escaped}[\\s>]`, 'g');

    const events = [];
    let m;

    while ((m = openRe.exec(text)) !== null) events.push({ type: 'open', index: m.index });
    while ((m = closeRe.exec(text)) !== null) events.push({ type: 'close', index: m.index });

    events.sort((a, b) => b.index - a.index); // reverse order

    let depth = 1;
    for (const ev of events) {
        if (ev.type === 'close') {
            depth++;
        } else {
            depth--;
            if (depth === 0) {
                const nameStart = ev.index + 1; // skip <
                return new vscode.Range(
                    document.positionAt(nameStart),
                    document.positionAt(nameStart + tagName.length)
                );
            }
        }
    }
    return null;
}

function activate(context) {
    // Register kiln.xsd with the XML language extension (redhat.vscode-xml)
    const schemaPath = vscode.Uri.joinPath(context.extensionUri, 'schemas', 'kiln.xsd').fsPath;
    const xmlConfig = vscode.workspace.getConfiguration('xml');
    const existing = xmlConfig.get('fileAssociations') ?? [];
    if (!existing.some(a => a.pattern === '**/*.kiln')) {
        xmlConfig.update(
            'fileAssociations',
            [...existing, { pattern: '**/*.kiln', systemId: schemaPath }],
            vscode.ConfigurationTarget.Global
        );
    }

    // Auto-close tags on >
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(async event => {
            if (event.document.languageId !== 'kiln') return;
            if (event.contentChanges.length !== 1) return;

            const change = event.contentChanges[0];
            if (change.text !== '>') return;

            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document !== event.document) return;

            const pos = change.range.start;
            const lineText = event.document.lineAt(pos.line).text;
            const upToGt = lineText.substring(0, pos.character + 1);

            const match = upToGt.match(/<([a-zA-Z][a-zA-Z0-9_-]*)(?:\s[^>]*)?>$/);
            if (!match) return;

            const tagName = match[1];
            const insertPos = new vscode.Position(pos.line, pos.character + 1);

            await editor.insertSnippet(
                new vscode.SnippetString(`$0</${tagName}>`),
                insertPos,
                { undoStopBefore: false, undoStopAfter: false }
            );
        })
    );

    // F2 rename — renames both opening and closing tag simultaneously
    context.subscriptions.push(
        vscode.languages.registerRenameProvider({ language: 'kiln' }, {
            prepareRename(document, position) {
                const info = getTagInfoAtPosition(document, position);
                if (!info) throw new Error('Place cursor on a tag name to rename');
                return { range: info.range, placeholder: info.tagName };
            },
            provideRenameEdits(document, position, newName) {
                const info = getTagInfoAtPosition(document, position);
                if (!info) return null;

                const edit = new vscode.WorkspaceEdit();
                edit.replace(document.uri, info.range, newName);

                const tagOffset = document.offsetAt(info.range.start);

                if (!info.isClose) {
                    const afterOpen = tagOffset + info.tagName.length;
                    const matchRange = findMatchingCloseTagRange(document, info.tagName, afterOpen);
                    if (matchRange) edit.replace(document.uri, matchRange, newName);
                } else {
                    const matchRange = findMatchingOpenTagRange(document, info.tagName, tagOffset);
                    if (matchRange) edit.replace(document.uri, matchRange, newName);
                }

                return edit;
            }
        })
    );
}

function deactivate() {}

module.exports = { activate, deactivate };
