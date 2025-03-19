import 'dart:io';

import 'package:dcmtopng_converter/provider/upload_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class FileUploadScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<FileUploadProvider>(context);

    return Scaffold(
      appBar: AppBar(title: Text("DICOM File Uploader")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            DragTarget<File>(
              onAcceptWithDetails: (file) {
                provider.selectedFile = file.data;
                provider.notifyListeners();
              },
              builder: (context, _, __) {
                return Container(
                  height: 150,
                  width: 300,
                  color: Colors.blue.shade100,
                  child: Center(
                    child: Text("Drag & Drop ZIP File Here"),
                  ),
                );
              },
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: provider.pickFile,
              child: Text("Select File"),
            ),
            if (provider.selectedFile != null) ...[
              Text("Selected: ${provider.selectedFile!.path}"),
              ElevatedButton(
                onPressed: provider.uploadFile,
                child: provider.isUploading ? CircularProgressIndicator() : Text("Upload"),
              ),
            ],
            if (provider.uploadStatus != null) Text(provider.uploadStatus!),
          ],
        ),
      ),
    );
  }
}