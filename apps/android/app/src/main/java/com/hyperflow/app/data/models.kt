package com.hyperflow.app.data

data class AgentSummary(val id: String, val role: String, val capability: String)
data class WorkflowSummary(val id: String, val name: String, val description: String)
data class RepoMetric(val label: String, val value: String)
data class LogEntry(val timestamp: String, val message: String)
