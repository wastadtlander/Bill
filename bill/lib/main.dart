import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

import 'camera/camera_function.dart';

late CameraDescription _firstCamera;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  _firstCamera = cameras.first;

  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'bill',
      theme: ThemeData(
        useMaterial3: true,
      ),
      home: const Home(),
      // home: UtilizeCamera(
      //   camera: firstCamera,
      // ),
    );
  }
}

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => Camera(
                  camera: _firstCamera,
                ),
              ),
            );
          },
          child: const Text('Scan Receipt'),
        ),
      ),
    );
  }
}
