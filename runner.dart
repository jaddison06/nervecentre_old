import 'dart:io';
import 'dart:convert';

void main() async {
  late final Process client;
  final server = await Process.start('dart', ['run', 'server/bin/main.dart']);
  server.stdout
    .transform(utf8.decoder)
    .forEach((line) async { if (line == 'Server intitialized\n') {
      print('Server initialized');
      client = await Process.start('dart', ['run', 'client/bin/main.dart']);
    }});


  // I have no idea what I'm doing
  await client.exitCode;
  await server.exitCode;
}