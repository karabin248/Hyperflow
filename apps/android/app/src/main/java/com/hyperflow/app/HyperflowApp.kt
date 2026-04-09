package com.hyperflow.app

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import com.hyperflow.app.ui.screens.DashboardScreen

@Composable
fun HyperflowApp() {
    MaterialTheme {
        Surface {
            DashboardScreen()
        }
    }
}
