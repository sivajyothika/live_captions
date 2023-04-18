import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:new_app/subtitle_screen.dart';
import 'package:video_player/video_player.dart';
import 'package:flutter_ffmpeg/flutter_ffmpeg.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:new_app/screens/signin_screen.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:http/http.dart' as http;

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final picker = ImagePicker();
  File? _pickedFile;
  VideoPlayerController? _controller;
  FlutterFFmpeg flutterFFmpeg = FlutterFFmpeg();

  String fileName = "";
  String RESULT = "";

  Future<void> _pickVideo() async {
    final pickedFile = await picker.pickVideo(source: ImageSource.gallery);
    setState(() {
      _pickedFile = File(pickedFile!.path);
      _controller = VideoPlayerController.file(_pickedFile!)
        ..initialize().then((_) {
          setState(() {});
          _controller!.play();
        });
    });

    // Upload the video file to Firebase Storage
    final storageReference = FirebaseStorage.instance
        .ref()
        .child('videos/${pickedFile!.path.split('/').last}');
    final uploadTask = storageReference.putFile(_pickedFile!);
    final snapshot = await uploadTask.whenComplete(() => null);
    final downloadUrl = await snapshot.ref.getDownloadURL();
    fileName = pickedFile.path.split('/').last;
  }

  // Future<void> predict() async {
  //   showDialog(
  //     context: this.context,
  //     builder: (context) {
  //       return const Center(child: CircularProgressIndicator());
  //     },
  //   );
  //   http.Response res = await http.get(Uri.parse(
  //       "https://fe1e-2405-201-c00e-b08c-fc-a17b-f63a-1831.in.ngrok.io/?query=$fileName"));
  //   var next = res.body;
  //   var decoded = jsonDecode(next);
  //   //return Text(decoded["output"]);
  //   Navigator.of(this.context).pop();
  //   setState(() {
  //     RESULT = decoded["output"];
  //   });
  Future predict() async {
    showDialog(
      context: this.context,
      builder: (context) {
        return const Center(child: CircularProgressIndicator());
      },
    );
    http.Response res = await http.get(
        Uri.parse("https://5bb4-183-82-111-80.in.ngrok.io/?query=$fileName"));
    var next = res.body;
    // var decoded = jsonDecode(next);
    // print(decoded);
    // Navigator.of(this.context).pop();
    // setState(() {
    //   RESULT = decoded["output"];
    // });
  }

  Future<void> _convertVideoToAudio() async {
    final audioFile = File('${_pickedFile!.path}.aac');
    final arguments =
        '-i ${_pickedFile!.path} -vn -acodec copy ${audioFile.path}';
    final executionId = await flutterFFmpeg.execute(arguments);
    print('FFmpeg execution id: $executionId');
    // Upload the audio file to Firebase Storage
    final storageReference =
        FirebaseStorage.instance.ref().child('audio/${audioFile.path}');
    final uploadTask = storageReference.putFile(audioFile);
    final snapshot = await uploadTask.whenComplete(() => null);
    final downloadUrl = await snapshot.ref.getDownloadURL();
  }

  @override
  void dispose() {
    _controller!.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MediaQuery(
        data: const MediaQueryData(),
        child: Scaffold(
          appBar: AppBar(
            title: const Text('Live Subtitles Generator'),
          ),
          body: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              _pickedFile == null
                  ? const Center(
                      child: Text('No video selected'),
                    )
                  : AspectRatio(
                      aspectRatio: _controller!.value.aspectRatio,
                      child: VideoPlayer(_controller!),
                    ),
              _controller != null && _controller!.value.isPlaying
                  ? IconButton(
                      onPressed: () {
                        setState(() {
                          _controller!.pause();
                        });
                      },
                      icon: Icon(Icons.pause),
                    )
                  : IconButton(
                      onPressed: () {
                        setState(() {
                          _controller!.play();
                        });
                      },
                      icon: Icon(Icons.play_arrow),
                    ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _pickVideo,
                child: const Text('Select video'),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _convertVideoToAudio,
                child: const Text('Convert to audio'),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: predict,
                child: Text('subtitled_video'),
              ),
              GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => subtitle()),
                  );
                },
                child: ElevatedButton(
                  onPressed: null,
                  child: Text('click for subtitle'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// class HomeScreen extends StatefulWidget {
//   const HomeScreen({Key? key}) : super(key: key);

//   @override
//   State<HomeScreen> createState() => _HomeScreenState();
// }

// class _HomeScreenState extends State<HomeScreen> {
//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       extendBodyBehindAppBar: true,
//       appBar: AppBar(
//         backgroundColor: Colors.transparent,
//         elevation: 0,
//         title: const Text(
//           "Welcome To Home Screen!!",
//           style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
//         ),
//       ),
//       body: Center(
//         child: ElevatedButton(
//           child: Text("Log Out"),
//           onPressed: () {
//             FirebaseAuth.instance.signOut().then((value) {
//               print("Signed Out");
//               Navigator.push(context,
//                   MaterialPageRoute(builder: (context) => SignInScreen()));
//             });
//           },
//         ),
//       ),
//     );
//   }
// }
