package com.example.ip_scanner

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.ip_scanner.ui.theme.IpscannerTheme
import java.io.IOException
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.util.function.Consumer


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            IpscannerTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    //modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    InputAndButton()
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Composable
fun InputAndButton(){
    var text by remember { mutableStateOf("") }
    var availableHostsConcatenated by remember { mutableStateOf("your ips will list here...") }

    //var availableHosts: MutableList<String>

    Column {
        OutlinedTextField(
            value = text,
            onValueChange = { text = it },
            label = { Text("Label") }
        )

        Button(onClick = {
            availableHostsConcatenated = lookForAvailableIps(text).joinToString("\n")
            }) {
            Text("Scan")
        }
        Text(
            text = availableHostsConcatenated,
            style = MaterialTheme.typography.bodyLarge
        )
    }
}

fun lookForAvailableIps(hostFormatWithPort: String): MutableList<String> {
    val split = hostFormatWithPort.split(":")
    val hostFormat = split[0]
    val port = split[1].toInt()
    val availableHosts: MutableList<String> = ArrayList()
    val threads: MutableList<Thread> = ArrayList(255)
    for (i in 0..254) {
        val host = java.lang.String.format(hostFormat, i)
        val t = Thread {
            try {
                val socket = Socket();
                val address: InetAddress = InetAddress.getAllByName(host)[0];
                socket.connect(InetSocketAddress(address, port), 300)
                availableHosts.add(host)
            } catch (e: IOException) {
                //ignore
            }
        }
        threads.add(t)
        t.start()
    }


    threads.forEach(Consumer { t: Thread ->
        try {
            t.join()
        } catch (e: InterruptedException) {
            throw RuntimeException(e)
        }
    })
    return availableHosts;
}