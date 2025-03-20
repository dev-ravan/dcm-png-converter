import 'dart:io';

import 'package:dcmtopng_converter/provider/upload_provider.dart';
import 'package:dcmtopng_converter/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => FileUploadProvider()),
      ],
      child: const MyApp(),
    ),
  );
}



class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DICOM Upload App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(
        

      ),
      home:  FileUploadScreen(),
    );
  }
}
