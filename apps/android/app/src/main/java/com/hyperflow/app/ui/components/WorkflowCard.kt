package com.hyperflow.app.ui.components

import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import com.hyperflow.app.data.WorkflowSummary

@Composable
fun WorkflowCard(workflow: WorkflowSummary) {
    Card {
        Text(text = workflow.name)
        Text(text = workflow.description)
    }
}
