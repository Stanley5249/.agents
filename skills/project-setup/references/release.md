# Release

- Only published projects, meaning they have a release tag or a registry package, keep a changelog. Generate it or the release notes with [`git-cliff`](https://git-cliff.org/) from Conventional Commits.
- Describe a release by its net change to the public API since the previous release. Leave out changes that a later change in the same release replaced.
- Changelogs and release notes may use emoji, such as in section headings.
