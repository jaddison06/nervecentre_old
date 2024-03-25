import 'dart:io';
import 'dart:convert';

extension on Stream<List<int>> {
  void passthrough([String prefix = '']) {
    transform(utf8.decoder)
      .transform(LineSplitter())
      .forEach((line) => print('$prefix$line'));
  }
}

void main() async {
  late final Process client;
  final server = await Process.start('dart', ['server/bin/server.dart']);
  server.stdout
    .transform(utf8.decoder)
    .transform(LineSplitter())
    .forEach((line) async {
      print('Server: $line');
      if (line == 'Initialized') {
        client = await Process.start('dart', ['client/bin/client.dart']);
        client.stdout.passthrough('Client: ');
        client.stderr.passthrough('Client: ');
      }
    });
  server.stderr.passthrough('Server: ');
}