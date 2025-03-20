import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class FileUploadProvider extends ChangeNotifier {
  File? selectedFile;
  bool isUploading = false;
  String? uploadStatus;
  List<String> imageUrls = [];

  void pickFile() async {
    try {
      if (Platform.isMacOS) {
        // macOS-specific implementation
        final result = await FilePicker.platform.pickFiles(
          type: FileType.any,
          allowMultiple: false,
          withReadStream: true, // This can help with macOS file handling
        );
        
        if (result != null && result.files.isNotEmpty) {
          selectedFile = File(result.files.single.path!);
          print("Selected File Path (macOS): ${selectedFile?.path}");
          notifyListeners();
        }
      } else {
        // Standard implementation for other platforms
        FilePickerResult? result = await FilePicker.platform.pickFiles(type: FileType.any);
        if (result != null) {
          selectedFile = File(result.files.single.path!);
          print("Selected File Path: ${selectedFile?.path}");
          notifyListeners();
        }
      }
    } catch (e) {
      print("Error picking file: $e");
      uploadStatus = "Error selecting file: ${e.toString()}";
      notifyListeners();
    }
  }

 Future<void> uploadFile() async {
  if (selectedFile == null) return;

  try {
    isUploading = true;
    uploadStatus = "Uploading...";
    notifyListeners();

    var request = http.MultipartRequest(
      'POST',
      Uri.parse('http://127.0.0.1:8000/converter/dicom-to-png/'),
    );

    request.files.add(await http.MultipartFile.fromPath('zip_file', selectedFile!.path));

    var streamedResponse = await request.send().timeout(Duration(seconds: 30));
    var response = await http.Response.fromStream(streamedResponse);

    isUploading = false;
    if (response.statusCode == 200) {
      var jsonResponse = jsonDecode(response.body);

    print("API Response: $jsonResponse");  // Check if 'stored_files' exists

if (jsonResponse['stored_files'] != null) {
  imageUrls = List<String>.from(jsonResponse['stored_files']);
} else {
  imageUrls = [];  // Handle null case
  print("Error: 'stored_files' is null");
}
 // Store image URLs
      uploadStatus = "Upload Successful";
    } else {
      uploadStatus = "Upload Failed (Status: ${response.statusCode})";
      print("Server response: ${response.body}");
    }
  } catch (e) {
    isUploading = false;
    uploadStatus = "Error during upload: ${e.toString()}";
    print("Upload error: $e");
  } finally {
    notifyListeners();
  }
}

}