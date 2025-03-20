
import 'package:dcmtopng_converter/provider/upload_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class FileUploadScreen extends StatelessWidget {
  const FileUploadScreen({super.key});

@override
Widget build(BuildContext context) {
  final provider = Provider.of<FileUploadProvider>(context);
  final imageUrls = provider.imageUrls;
  return Scaffold(
    appBar: AppBar(title: Text("DICOM File Uploader")),
    body: SingleChildScrollView(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            OutlinedButton(
              style: OutlinedButton.styleFrom(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6))),
              onPressed: provider.pickFile,
              child: Text("Select File"),
            ),
            SizedBox(height: 16,),
            if (provider.selectedFile != null) ...[
              Text("Selected: ${provider.selectedFile!.path}"),
               SizedBox(height: 16,),
              OutlinedButton(
                 style: OutlinedButton.styleFrom(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6))),
                onPressed: provider.uploadFile,
                child: provider.isUploading 
                  ? SizedBox(
                      width: 20, 
                      height: 20, 
                      child: CircularProgressIndicator(strokeWidth: 2)
                    ) 
                  : Text("Upload"),
              ),
            ],
             SizedBox(height: 16,),
            
            if (provider.uploadStatus != null) Text(provider.uploadStatus!),
      
            imageUrls.isEmpty
            ? Center(child: Text("No images found"))
            : GridView.builder(
              shrinkWrap: true,
                padding: EdgeInsets.all(10),
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 4,
                  crossAxisSpacing: 10,
                  mainAxisSpacing: 10,
                ),
                itemCount: imageUrls.length,
                itemBuilder: (context, index) {
                  return Image.network(
                    imageUrls[index],
                    fit: BoxFit.fitWidth,
                  );
                },
              ),
      
          ],
        ),
      ),
    ),
  );
}
}