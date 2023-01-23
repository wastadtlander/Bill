import 'package:bill/main.dart';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class Camera extends StatefulWidget {
  const Camera({
    super.key,
    required this.camera,
  });

  final CameraDescription camera;

  @override
  CameraState createState() => CameraState();
}

class CameraState extends State<Camera> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.max,
    );

    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<void>(
      future: _initializeControllerFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          return CameraWrapper(controller: _controller);
        } else {
          return const Center(child: CircularProgressIndicator());
        }
      },
    );
  }
}

class CameraWrapper extends StatelessWidget {
  const CameraWrapper({
    Key? key,
    required CameraController controller,
  })  : _controller = controller,
        super(key: key);

  final CameraController _controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Container(
        padding: const EdgeInsets.all(8.0),
        child: ClipRRect(
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(8.0),
            topRight: Radius.circular(8.0),
            bottomRight: Radius.circular(8.0),
            bottomLeft: Radius.circular(8.0),
          ),
          child: CameraPreview(_controller),
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        shape: const CircularNotchedRectangle(),
        child: Container(height: 50.0),
      ),
      floatingActionButton: const FloatingActionButton(
        onPressed: null,
        shape: CircleBorder(),
        child: Icon(Icons.camera_alt),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endDocked,
    );
  }
}
