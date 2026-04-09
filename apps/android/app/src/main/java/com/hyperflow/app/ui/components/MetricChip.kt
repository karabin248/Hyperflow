package com.hyperflow.app.ui.components

import androidx.compose.material3.AssistChip
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import com.hyperflow.app.data.RepoMetric

@Composable
fun MetricChip(metric: RepoMetric) {
    AssistChip(onClick = {}, label = { Text("${metric.label}: ${metric.value}") })
}
