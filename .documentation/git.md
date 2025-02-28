# Git

## Signing Commits With SSH Key

```bash
git commit --gpg-sign --message
```

## GNU Privacy Guard (GPG)

```bash
gpg --full-generate-key
```

```bash
gpg --list-keys
```

```bash
gpg --list-secret-keys
```

```bash
gpg --fingerprint
```

```bash
gpg --armor --export email@example.com
```

```bash
gpg --armor --export-secret-keys email@example.com
```

```bash
gpg --armor --export-secret-keys your-email@example.com > private-key.asc
```

```bash
gpg --list-secret-keys --keyid-format LONG
```