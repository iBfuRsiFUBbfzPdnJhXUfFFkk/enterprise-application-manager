import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from gitlab_sync.models import (
    GitLabSyncCommit,
    GitLabSyncEpic,
    GitLabSyncGroup,
    GitLabSyncIssue,
    GitLabSyncJob,
    GitLabSyncMergeRequest,
    GitLabSyncPipeline,
    GitLabSyncProject,
    GitLabSyncRepository,
    GitLabSyncUser,
    GitLabSyncVulnerability,
)


class Command(BaseCommand):
    help = "Creates test data for GitLab Sync entities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing test data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing GitLab sync data...")
            GitLabSyncVulnerability.objects.all().delete()
            GitLabSyncJob.objects.all().delete()
            GitLabSyncCommit.objects.all().delete()
            GitLabSyncMergeRequest.objects.all().delete()
            GitLabSyncIssue.objects.all().delete()
            GitLabSyncEpic.objects.all().delete()
            GitLabSyncPipeline.objects.all().delete()
            GitLabSyncRepository.objects.all().delete()
            GitLabSyncProject.objects.all().delete()
            GitLabSyncUser.objects.all().delete()
            GitLabSyncGroup.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Cleared existing data"))

        self.stdout.write("Creating test data...")

        # Create groups
        groups = self.create_groups()
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(groups)} groups"))

        # Create users
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(users)} users"))

        # Create projects
        projects = self.create_projects(groups)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(projects)} projects"))

        # Create repositories
        repositories = self.create_repositories(projects)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(repositories)} repositories")
        )

        # Create epics
        epics = self.create_epics(groups, users)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(epics)} epics"))

        # Create issues
        issues = self.create_issues(projects, users, epics)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(issues)} issues"))

        # Create pipelines
        pipelines = self.create_pipelines(projects, users)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(pipelines)} pipelines"))

        # Create jobs
        jobs = self.create_jobs(pipelines, projects, users)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(jobs)} jobs"))

        # Create commits
        commits = self.create_commits(projects, repositories, users)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(commits)} commits"))

        # Create merge requests
        merge_requests = self.create_merge_requests(projects, users, pipelines)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(merge_requests)} merge requests")
        )

        # Create vulnerabilities
        vulnerabilities = self.create_vulnerabilities(projects, users)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(vulnerabilities)} vulnerabilities")
        )

        self.stdout.write(
            self.style.SUCCESS("\n✓ Successfully created all test data!")
        )

    def create_groups(self):
        groups = []
        group_names = [
            ("Engineering", "engineering"),
            ("Product", "product"),
            ("Design", "design"),
            ("Infrastructure", "infrastructure"),
            ("Security", "security"),
        ]

        for idx, (name, path) in enumerate(group_names, start=1000):
            group = GitLabSyncGroup.objects.create(
                id=idx,
                name=name,
                full_name=f"Company / {name}",
                path=path,
                full_path=f"company/{path}",
                visibility=random.choice(["private", "internal", "public"]),
                web_url=f"https://gitlab.com/company/{path}",
                created_at=timezone.now() - timedelta(days=random.randint(100, 500)),
            )
            groups.append(group)

        return groups

    def create_users(self):
        users = []
        user_data = [
            ("Alice Johnson", "alice.johnson", "alice@example.com"),
            ("Bob Smith", "bob.smith", "bob@example.com"),
            ("Carol Davis", "carol.davis", "carol@example.com"),
            ("David Wilson", "david.wilson", "david@example.com"),
            ("Eve Martinez", "eve.martinez", "eve@example.com"),
            ("Frank Brown", "frank.brown", "frank@example.com"),
            ("Grace Lee", "grace.lee", "grace@example.com"),
            ("Henry Taylor", "henry.taylor", "henry@example.com"),
        ]

        for idx, (name, username, email) in enumerate(user_data, start=2000):
            user = GitLabSyncUser.objects.create(
                id=idx,
                username=username,
                name=name,
                email=email,
                state="active",
                web_url=f"https://gitlab.com/{username}",
                created_at=timezone.now() - timedelta(days=random.randint(200, 600)),
            )
            users.append(user)

        return users

    def create_projects(self, groups):
        projects = []
        project_names = [
            "web-frontend",
            "api-backend",
            "mobile-app",
            "data-pipeline",
            "ml-models",
            "infrastructure-config",
            "design-system",
            "documentation",
            "monitoring-tools",
            "auth-service",
        ]

        for idx, project_name in enumerate(project_names, start=3000):
            group = random.choice(groups)
            project = GitLabSyncProject.objects.create(
                id=idx,
                name=project_name.replace("-", " ").title(),
                path=project_name,
                path_with_namespace=f"{group.path}/{project_name}",
                name_with_namespace=f"{group.name} / {project_name.replace('-', ' ').title()}",
                visibility=random.choice(["private", "internal", "public"]),
                description=f"Description for {project_name} project",
                default_branch="main",
                group=group,
                web_url=f"https://gitlab.com/{group.path}/{project_name}",
                created_at=timezone.now() - timedelta(days=random.randint(50, 400)),
                last_activity_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                updated_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                star_count=random.randint(0, 50),
                forks_count=random.randint(0, 20),
            )
            projects.append(project)

        return projects

    def create_repositories(self, projects):
        repositories = []
        for project in projects:
            repo = GitLabSyncRepository.objects.create(
                id=project.id,
                project=project,
            )
            repositories.append(repo)
        return repositories

    def create_epics(self, groups, users):
        epics = []
        epic_titles = [
            "Q1 2024 Roadmap",
            "Platform Modernization",
            "Mobile App Redesign",
            "Security Improvements",
            "Performance Optimization",
            "User Experience Enhancements",
        ]

        for idx, title in enumerate(epic_titles, start=4000):
            group = random.choice(groups)
            author = random.choice(users)
            created = timezone.now() - timedelta(days=random.randint(30, 200))

            epic = GitLabSyncEpic.objects.create(
                id=idx,
                iid=idx - 3999,
                group=group,
                title=title,
                description=f"Epic description for {title}",
                state=random.choice(["opened", "opened", "opened", "closed"]),
                author=author,
                web_url=f"https://gitlab.com/groups/{group.path}/-/epics/{idx-3999}",
                created_at=created,
                updated_at=created + timedelta(days=random.randint(1, 20)),
            )
            epics.append(epic)

        return epics

    def create_issues(self, projects, users, epics):
        issues = []
        issue_templates = [
            ("Bug: Login fails with special characters", "bug", "high"),
            ("Feature: Add dark mode support", "issue", "medium"),
            ("Bug: Memory leak in data processing", "bug", "critical"),
            ("Feature: Export to CSV functionality", "issue", "low"),
            ("Bug: Incorrect timezone handling", "bug", "medium"),
            ("Feature: Multi-language support", "issue", "high"),
            ("Bug: Broken links in documentation", "bug", "low"),
            ("Feature: Real-time notifications", "issue", "medium"),
            ("Incident: Database connection timeout", "incident", "critical"),
            ("Feature: Advanced search filters", "issue", "medium"),
        ]

        for idx, (title, issue_type, severity) in enumerate(
            issue_templates * 3, start=5000
        ):
            project = random.choice(projects)
            author = random.choice(users)
            created = timezone.now() - timedelta(days=random.randint(1, 100))
            state = random.choice(
                ["opened", "opened", "opened", "closed", "closed"]
            )

            issue = GitLabSyncIssue.objects.create(
                id=idx,
                iid=idx - 4999,
                project=project,
                group=project.group,
                title=f"{title} #{idx-4999}",
                description=f"Detailed description for {title}",
                state=state,
                type=issue_type,
                issue_type=issue_type,
                severity=severity,
                author=author,
                web_url=f"https://gitlab.com/{project.path_with_namespace}/-/issues/{idx-4999}",
                created_at=created,
                updated_at=created + timedelta(days=random.randint(0, 20)),
                closed_at=created + timedelta(days=random.randint(5, 30))
                if state == "closed"
                else None,
                weight=random.randint(1, 5),
                user_notes_count=random.randint(0, 15),
                confidential=random.choice([True, False, False, False]),
            )

            # Link some issues to epics
            if random.random() < 0.3 and epics:
                issue.epic = random.choice(epics)
                issue.save()

            # Add assignees
            if random.random() < 0.7:
                assignee_count = random.randint(1, 2)
                assignees = random.sample(users, min(assignee_count, len(users)))
                issue.assignees.set(assignees)

            issues.append(issue)

        return issues

    def create_pipelines(self, projects, users):
        pipelines = []
        statuses = ["success", "failed", "running", "pending", "canceled"]
        status_weights = [50, 20, 5, 10, 15]

        for idx in range(6000, 6100):
            project = random.choice(projects)
            user = random.choice(users)
            status = random.choices(statuses, weights=status_weights)[0]
            created = timezone.now() - timedelta(days=random.randint(1, 60))

            pipeline = GitLabSyncPipeline.objects.create(
                id=idx,
                project=project,
                status=status,
                ref=random.choice(["main", "develop", "feature/new-feature"]),
                sha=f"{''.join(random.choices('abcdef0123456789', k=40))}",
                web_url=f"https://gitlab.com/{project.path_with_namespace}/-/pipelines/{idx}",
                user=user,
                created_at=created,
                updated_at=created + timedelta(minutes=random.randint(5, 120)),
                duration=random.randint(60, 3600) if status in ["success", "failed"] else None,
                coverage=round(random.uniform(70, 95), 2)
                if status == "success"
                else None,
                source=random.choice(["push", "web", "trigger", "schedule"]),
            )
            pipelines.append(pipeline)

        return pipelines

    def create_jobs(self, pipelines, projects, users):
        jobs = []
        job_names = [
            "build",
            "test:unit",
            "test:integration",
            "lint",
            "security-scan",
            "deploy:staging",
            "deploy:production",
        ]
        stages = ["build", "test", "security", "deploy"]

        for idx in range(7000, 7200):
            pipeline = random.choice(pipelines)
            job_name = random.choice(job_names)
            status = pipeline.status if random.random() < 0.8 else random.choice(["success", "failed"])
            created = pipeline.created_at + timedelta(minutes=random.randint(0, 10))

            job = GitLabSyncJob.objects.create(
                id=idx,
                name=job_name,
                stage=random.choice(stages),
                status=status,
                pipeline=pipeline,
                project=pipeline.project,
                user=pipeline.user,
                web_url=f"https://gitlab.com/{pipeline.project.path_with_namespace}/-/jobs/{idx}",
                created_at=created,
                started_at=created + timedelta(seconds=random.randint(5, 60)),
                finished_at=created + timedelta(minutes=random.randint(1, 30))
                if status in ["success", "failed"]
                else None,
                duration=random.uniform(60, 1800) if status in ["success", "failed"] else None,
                coverage=round(random.uniform(70, 95), 2)
                if status == "success" and "test" in job_name
                else None,
            )
            jobs.append(job)

        return jobs

    def create_commits(self, projects, repositories, users):
        commits = []
        commit_messages = [
            "feat: add new authentication method",
            "fix: resolve memory leak issue",
            "docs: update README with examples",
            "refactor: simplify database queries",
            "test: add unit tests for API",
            "chore: update dependencies",
            "style: format code with prettier",
            "perf: optimize image loading",
        ]

        for idx in range(50):
            project = random.choice(projects)
            repository = next((r for r in repositories if r.project == project), None)
            author = random.choice(users)
            message = random.choice(commit_messages)
            created = timezone.now() - timedelta(days=random.randint(1, 90))
            sha = "".join(random.choices("abcdef0123456789", k=40))

            commit = GitLabSyncCommit.objects.create(
                sha=sha,
                project=project,
                repository=repository,
                title=message,
                message=f"{message}\n\nDetailed commit message with more information.",
                author_name=author.name,
                author_email=author.email,
                author=author,
                committer_name=author.name,
                committer_email=author.email,
                web_url=f"https://gitlab.com/{project.path_with_namespace}/-/commit/{sha}",
                created_at=created,
                authored_date=created,
                committed_date=created,
                additions=random.randint(10, 500),
                deletions=random.randint(5, 200),
                total_changes=random.randint(15, 700),
            )
            commits.append(commit)

        return commits

    def create_merge_requests(self, projects, users, pipelines):
        merge_requests = []
        mr_titles = [
            "Add user authentication feature",
            "Fix critical security vulnerability",
            "Refactor database models",
            "Update documentation for API",
            "Implement caching layer",
            "Add integration tests",
            "Improve error handling",
            "Optimize query performance",
        ]

        for idx, title in enumerate(mr_titles * 4, start=8000):
            project = random.choice(projects)
            author = random.choice(users)
            created = timezone.now() - timedelta(days=random.randint(1, 60))
            state = random.choice(
                ["opened", "opened", "merged", "merged", "merged", "closed"]
            )

            mr = GitLabSyncMergeRequest.objects.create(
                id=idx,
                iid=idx - 7999,
                project=project,
                title=f"{title} (!{idx-7999})",
                description=f"This MR implements {title.lower()}",
                state=state,
                source_branch=f"feature/{title.lower().replace(' ', '-')}",
                target_branch="main",
                author=author,
                web_url=f"https://gitlab.com/{project.path_with_namespace}/-/merge_requests/{idx-7999}",
                created_at=created,
                updated_at=created + timedelta(days=random.randint(0, 10)),
                merged_at=created + timedelta(days=random.randint(1, 15))
                if state == "merged"
                else None,
                closed_at=created + timedelta(days=random.randint(1, 15))
                if state in ["merged", "closed"]
                else None,
                draft=random.choice([True, False, False, False]),
                user_notes_count=random.randint(0, 20),
                upvotes=random.randint(0, 10),
                downvotes=random.randint(0, 2),
                has_conflicts=random.choice([True, False, False, False, False]),
            )

            # Link to pipeline
            if random.random() < 0.8 and pipelines:
                mr.head_pipeline = random.choice(
                    [p for p in pipelines if p.project == project]
                )
                mr.save()

            # Add assignees and reviewers
            if random.random() < 0.8:
                assignee_count = random.randint(1, 2)
                assignees = random.sample(users, min(assignee_count, len(users)))
                mr.assignees.set(assignees)

            if random.random() < 0.6:
                reviewer_count = random.randint(1, 2)
                reviewers = random.sample(users, min(reviewer_count, len(users)))
                mr.reviewers.set(reviewers)

            merge_requests.append(mr)

        return merge_requests

    def create_vulnerabilities(self, projects, users):
        vulnerabilities = []
        vulnerability_data = [
            ("SQL Injection in user input", "high", "detected"),
            ("Cross-Site Scripting (XSS)", "medium", "confirmed"),
            ("Insecure Direct Object Reference", "high", "resolved"),
            ("Missing Authentication", "critical", "detected"),
            ("Weak Password Policy", "medium", "dismissed"),
            ("Sensitive Data Exposure", "high", "confirmed"),
            ("Broken Access Control", "critical", "detected"),
            ("Security Misconfiguration", "medium", "resolved"),
            ("Using Components with Known Vulnerabilities", "high", "detected"),
            ("Insufficient Logging", "low", "dismissed"),
        ]

        for idx, (title, severity, state) in enumerate(
            vulnerability_data * 2, start=9000
        ):
            project = random.choice(projects)
            author = random.choice(users)
            detected = timezone.now() - timedelta(days=random.randint(1, 120))

            vuln = GitLabSyncVulnerability.objects.create(
                id=idx,
                project=project,
                title=f"{title} - {project.name}",
                description=f"Vulnerability description: {title}",
                severity=severity,
                state=state,
                author=author,
                detected_at=detected,
                confidence="high",
            )

            if state == "resolved":
                vuln.resolved_at = detected + timedelta(days=random.randint(1, 30))
                vuln.resolved_by = random.choice(users)
                vuln.save()
            elif state == "dismissed":
                vuln.dismissed_at = detected + timedelta(days=random.randint(1, 15))
                vuln.dismissed_by = random.choice(users)
                vuln.save()

            vulnerabilities.append(vuln)

        return vulnerabilities
