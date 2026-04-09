package com.hyperflow.app.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.runtime.Composable
import androidx.compose.material3.Text
import com.hyperflow.app.data.FakeRepository
import com.hyperflow.app.ui.components.AgentCard
import com.hyperflow.app.ui.components.MetricChip
import com.hyperflow.app.ui.components.WorkflowCard

@Composable
fun SettingsScreen() {
    Column {
        Text("Settings")
        Text("Backend URL: local fake data")
    }
}
