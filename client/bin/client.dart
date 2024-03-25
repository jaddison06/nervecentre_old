import '../generated.dart';
import 'package:ffi/ffi.dart';
import 'dart:ffi';

void main(List<String> arguments) {
  final (x, y) = (malloc.allocate<Int32>(4), malloc.allocate<Int32>(4));
  x.value = 20;
  y.value = 20;
  final display = SDLDisplayRaw('Nerve Center', true);
  final event = SDLEventRaw();
  var quit = false;
  while (!quit) {
    while (event.Poll() > 0) {
      if (event.type == EventType.Quit) quit = true;
      else if (event.type == EventType.MouseMove) event.GetPos(x, y);
      else if (event.type == EventType.Key && event.key == Key.Escape) quit = true;
    }
    display.DrawRect(x.value, y.value, 250, 150, 255, 0, 0, 255);
    display.Flush();
    display.Clear(0, 0, 0, 255);
  }
  event.Destroy();
  // Calls SDL_Quit()
  display.Destroy();
}
