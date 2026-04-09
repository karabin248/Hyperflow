package com.hyperflow.app.ui.components

import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import com.hyperflow.app.data.AgentSummary

@Composable
fun AgentCard(agent: AgentSummary) {
    Card {
        Text(text = "${agent.role}: ${agent.capability}")
    }
}
