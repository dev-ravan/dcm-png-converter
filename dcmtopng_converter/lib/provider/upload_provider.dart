import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class FileUploadProvider extends ChangeNotifier {
  File? selectedFile;
  bool isUploading = false;
  String? uploadStatus;

  void pickFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(type: FileType.any);
    if (result != null) {
      selectedFile = File(result.files.single.path!);
      print("Selected File Path: ${selectedFile?.path}");

      notifyListeners();
    }
  }

  Future<void> uploadFile() async {
    if (selectedFile == null) return;
    isUploading = true;
    uploadStatus = "Uploading...";
    notifyListeners();
    
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('http://localhost:8000/converter/dicom_to_png'),
    );
    request.files.add(await http.MultipartFile.fromPath('file', selectedFile!.path));
    var response = await request.send();
    
    isUploading = false;
    uploadStatus = response.statusCode == 200 ? "Upload Successful" : "Upload Failed";
    notifyListeners();
  }
}