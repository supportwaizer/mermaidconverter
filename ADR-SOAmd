# ADR-002: Use Git for Source Code Control
 
| Field | Value |
|---|---|
| **Status** | Proposed |
| **Date** | 2026-08-05 |
| **Deciders** | *[Architecture group / tech leads]* |
| **Consulted** | *[Platform, SRE, Security, Compliance]* |
| **Informed** | *[Engineering org]* |
| **Supersedes** | *[ADR-00X: Subversion as VCS, if applicable]* |
 
---
 
## 1. Context
 
*[Replace bracketed text with your specifics.]*
 
The team currently uses *[Subversion / TFVC / shared network drives / no formal VCS]* across *[K]* teams and *[N]* developers, *[X]* of whom work remotely or across time zones.
 
Forces driving a decision now:
 
- **Multiple independently released components.** The codebase produces *[N]* components with different release cadences, and the current setup forces them onto a single release train.
- **Centralised VCS blocks offline and parallel work.** Committing requires server connectivity; branching is expensive enough that developers avoid it and accumulate large uncommitted changes.
- **Code review is not enforceable.** There is no mechanism to require review before code reaches a release line, which is a gap against *[SOC 2 / ISO 27001 / internal audit]* requirements for change control.
- **CI/CD tooling assumes Git.** *[GitHub Actions / GitLab CI / Jenkins / Argo CD]* and most modern supply-chain tooling (dependency scanning, SBOM generation, signed provenance) are built around Git webhooks and commit SHAs.
- **Hiring and onboarding.** Git is the de facto industry standard; non-Git tooling adds friction for every new hire.
Note that the *choice of Git itself* is close to a foregone conclusion in 2026. The substance of this decision — and the part that will actually be contested later — is the **hosting platform, repository topology, and branching model**. This ADR records all four so the reasoning survives.
 
## 2. Decision
 
**We will use Git as the version control system for all source code, infrastructure definitions, and configuration.**
 
Concretely:
 
1. **Hosting.** Repositories are hosted on *[GitHub Enterprise / GitLab / Bitbucket / Azure Repos]* under the *[org name]* organisation. Self-hosting is not adopted; we accept the managed-service dependency in exchange for not operating the platform.
2. **Repository topology: one repository per independently deployable component.** Each component with its own release cadence gets its own repository, plus separate repositories for shared libraries, infrastructure-as-code, and documentation. Repository boundaries follow deployment and ownership boundaries, so access control, review routing, and version tagging all align with the team accountable for the code.
3. **Branching model: trunk-based development with short-lived branches.** A single long-lived `main` branch, always releasable. Feature branches live no longer than *[2 days]* and merge via pull request. Release branches are cut from `main` only when a release must be patched independently. We explicitly reject long-lived `develop`/`release`/`hotfix` branch hierarchies (Gitflow) as unnecessary overhead for continuously deployed software.
4. **`main` is protected.** Direct pushes are blocked. Merges require: at least *[1]* approving review, passing CI, and up-to-date-with-base. Force-push and branch deletion on `main` are disabled.
5. **Commit hygiene.** Conventional Commits format (`feat:`, `fix:`, `chore:`) to enable automated changelog and semantic version derivation. Commits are signed *[GPG / SSH / Sigstore]* to establish authorship provenance.
6. **Ownership.** A `CODEOWNERS` file in each repository routes review requests to the owning team, so review responsibility is enforced by tooling rather than left to convention.
7. **What does not go in Git.** Secrets (use *[Vault / AWS Secrets Manager]*), build artefacts, and large binaries. Binary assets over *[100 MB]* use Git LFS. Secret scanning and push protection are enabled at the organisation level.
## 3. Alternatives Considered
 
| Option | Why not chosen |
|---|---|
| **Stay on Subversion / TFVC** | Centralised model requires connectivity to commit, makes branching costly, and is unsupported by most modern CI/CD and supply-chain tooling. Migration cost is paid once; the friction is paid daily. |
| **Mercurial** | Comparable distributed model and arguably a gentler CLI, but a far smaller ecosystem, declining hosting support, and a much smaller hiring pool. No advantage large enough to offset that. |
| **Perforce Helix Core** | Genuinely better for very large binary assets and file locking (its strength in game and hardware development). Our repositories are predominantly text; we would pay licensing and operational cost for a capability we do not need. |
| **Monorepo (single Git repository)** | Simplifies cross-component refactoring and atomic changes across boundaries, and remains a defensible choice. Rejected here because it puts every team on a shared pipeline and shared release coordination, and because efficient monorepo builds require tooling (*[Bazel / Nx / Turborepo]*) we do not currently run. **Revisit if cross-component change coordination becomes the dominant cost.** |
| **Gitflow branching** | Long-lived parallel branches produce merge debt and delay integration. Justified when shipping versioned, installed software on a slow release cycle; we deploy continuously. |
 
## 4. Consequences
 
### Positive
 
- Full local history: branching, diffing, blame, and bisect work offline and are fast enough to use routinely.
- Pull requests give an auditable, enforced review gate satisfying change-control requirements — reviewer identity, timestamp, and approving decision are recorded immutably.
- Commit SHAs give an immutable build identity, enabling reproducible builds and traceability from a running artefact back to source.
- The entire CI/CD, security-scanning, and GitOps ecosystem works out of the box.
- Repository-per-component maps ownership boundaries directly onto access control and review routing.
### Negative
 
- **Learning curve.** Git's model (staging area, rebase vs merge, detached HEAD) is genuinely confusing for newcomers. Budget for training; expect recoverable mistakes in the first *[quarter]*.
- **History is rewritable.** `push --force` and `filter-repo` can destroy history. Mitigated by branch protection on `main`, but developers can still damage their own branches.
- **Poor with large binaries.** Every clone pulls full history; large binaries bloat repositories permanently, and Git LFS is a partial fix with its own operational cost. Committing a large file is effectively irreversible without rewriting history.
- **No file locking.** Two people editing the same binary asset produce an unmergeable conflict. Relevant if *[design assets / documents]* enter the repository.
- **Repository sprawl.** Repository-per-component means *[N]* sets of settings, branch protections, and CI configs. Without templating and org-level policy, these drift.
- **Cross-cutting changes span repositories.** A change touching three components requires three coordinated pull requests with no atomic merge. This is the main cost of polyrepo and the main argument for revisiting a monorepo.
- **Migration cost.** Converting *[SVN]* history, retraining, and rewiring pipelines is a *[N-week]* effort with a period of dual-running.
### Neutral / Follow-on
 
- Repository topology can change later; the migration from polyrepo to monorepo (or back) is disruptive but well-trodden.
- The hosting platform is the stickiest part of this decision — issues, pull request history, CI configuration, and permissions are only partially portable.
## 5. Implementation Notes
 
- **Migration:** convert history with *[`git-svn` / `svn2git`]*, preserving author mapping. Run both systems read/write for *[1 sprint]*, then make the old system read-only rather than deleting it.
- **Repository template:** create a template repository carrying the standard `.gitignore`, `CODEOWNERS`, PR template, branch protection, and CI skeleton. New repositories are created from it, not from scratch.
- **Org-level policy:** branch protection rules, secret scanning, and required status checks are set as organisation policy where the platform supports it, so per-repository drift is not possible.
- **Training:** a *[half-day]* workshop covering rebase vs merge, resolving conflicts, and recovery via `reflog`. The recovery topic matters most — most Git fear is fear of unrecoverable loss.
- **Backups:** the managed platform is not a backup. Mirror all repositories to *[secondary location]* on a *[daily]* schedule.
## 6. Compliance and Enforcement
 
- Branch protection on `main` in every repository; verified by a scheduled audit script, not by trust.
- Pre-commit hooks *[e.g. pre-commit, gitleaks]* block secrets and oversized files before they reach history.
- CI fails on unsigned commits *[if signing is mandated]* and on non-conforming commit messages.
- Quarterly access review: repository permissions reconciled against team membership.
## 7. Review Triggers
 
Revisit this decision if:
 
- Coordinating cross-repository changes becomes a routine source of delay → reconsider a monorepo.
- Binary assets become a significant fraction of repository size → reconsider Git LFS strategy or a dedicated asset store.
- The hosting platform's availability or pricing materially changes the calculus.
- Repository count crosses *[N]*, making per-repository configuration drift unmanageable without further automation.
