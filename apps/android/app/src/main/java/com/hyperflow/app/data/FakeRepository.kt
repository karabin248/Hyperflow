package com.hyperflow.app.data

object FakeRepository {
    fun agents() = listOf(
        AgentSummary("research-worker", "research", "evidence gathering"),
        AgentSummary("reasoning-worker", "reasoning", "plan and synthesis"),
        AgentSummary("reporting-worker", "reporting", "status and release reporting"),
        AgentSummary("tools-worker", "tools", "runtime helper tools")
    )

    fun workflows() = listOf(
        WorkflowSummary("repo-audit", "Repository Audit", "Inspect repository structure and risks."),
        WorkflowSummary("canonical-build", "Canonical Build", "Create or repair the canonical repository shape."),
        WorkflowSummary("release-report", "Release Report", "Summarize operational health and release readiness.")
    )

    fun metrics() = listOf(
        RepoMetric("Backend", "Ready"),
        RepoMetric("API", "Ready"),
        RepoMetric("Android", "Skeleton"),
        RepoMetric("Docs", "Ready")
    )

    fun logs() = listOf(
        LogEntry("2026-03-22T09:00:00Z", "Canonical repo scaffold created."),
        LogEntry("2026-03-22T09:05:00Z", "Backend API routes wired."),
        LogEntry("2026-03-22T09:10:00Z", "Docs synchronized with runtime surface.")
    )
}
