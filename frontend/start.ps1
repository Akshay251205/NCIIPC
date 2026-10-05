param(
    [ValidateSet('dev', 'build', 'lint', 'preview')]
    [string]$Command = 'dev'
)

$node = 'C:\Program Files\nodejs\node.exe'
$npmCli = 'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js'

if (-not (Test-Path -LiteralPath $node) -or -not (Test-Path -LiteralPath $npmCli)) {
    throw 'Node.js/npm was not found. Install Node.js LTS, then run npm install in frontend.'
}

& $node $npmCli run $Command
exit $LASTEXITCODE
