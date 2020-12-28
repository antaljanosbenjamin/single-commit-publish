# Single commit publish
This action can be used to publish files to the specified branch of a Github repository in a single commit with *force push to erase history*.

## Inputs

In general the `source-dir`, `files-and-dirs`, `author-name` and `commit-message` parameters can contain values with spaces, but for `files-and-dirs` such paths must be escaped by using double quotes. For the exact usage please check the [example](#example-usage).

### `github-token` (required)
GitHub token to use for push operation.

### `github-actor`
GitHub username to use for push operation. Defaults to `${{ github.actor }}`.
### `github-repository`
The GitHub repository to where the files should be published in `<username/repo>` format. Defaults to `${{ github.repository }}`.

### `branch` (required)
The branch to where the files should be published.

### `source-dir`
The source directory that contains all the files and directories that are going to be published. The directory structure inside this folder is going to be kept for the published files and directories. Defaults to `${{ github.workspace }}`.

### `files-and-dirs` (required)
List of paths (relative or absolute) of the files and directories to publish. They must be inside the source directory. The directory structure relative to source directory is kept for publishing.

### `author-name`
The name that will appear in the commit. Defaults to `github-actions`.

### `author-email`
The email that will appear in the commit. Defaults to `github-actions@noreply.github.com`.

### `commit-message`
The commit message that will appear in the commit. Defaults to `"Publish from #${{ github.run_number }}"`.

## Example usage
```
name: test
on: [push]
jobs:
  test-example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: 'cd test'
        shell: bash
      - uses: antaljanosbenjamin/single-commit-publish@master
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          branch: test-example-published-files
          source-dir: test
          files-and-dirs: 'a.txt b.txt some_dir "file with space.txt" "directory with space"'
```

For further examples check the [test workflow](.github/workflows/test.yml).