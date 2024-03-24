// for native types & basic FFI functionality
import 'dart:ffi';
// for string utils
import 'package:ffi/ffi.dart';
// for @mustCallSuper
import 'package:meta/meta.dart';

// ----------FILE: CLIENT/NATIVE\CLIENTHELLO.GEN----------

// ----------FUNCTION SIGNATURE TYPEDEFS----------

// void ClientHello()
typedef _libClientHello_func_ClientHello_native_sig = Void Function();
typedef _libClientHello_func_ClientHello_sig = void Function();

// ----------LIBCLIENTHELLO----------

class libClientHello {

    static _libClientHello_func_ClientHello_sig? _ClientHello;

    void _initRefs() {
        if (
            _ClientHello == null
        ) {
            final lib = DynamicLibrary.open('build\\objects\\client/native\\libClientHello.dll');

            _ClientHello = lib.lookupFunction<_libClientHello_func_ClientHello_native_sig, _libClientHello_func_ClientHello_sig>('ClientHello');
        }
    }

    libClientHello() {
        _initRefs();
    }

    void ClientHello() {
        return _ClientHello!();
    }

}


// ----------FILE: SHARED/NATIVE\NATIVEHELLO.GEN----------

// ----------FUNCTION SIGNATURE TYPEDEFS----------

// int NativeHello(int arg1, char* arg2)
typedef _libNativeHello_func_NativeHello_native_sig = Int32 Function(Int32, Pointer<Utf8>);
typedef _libNativeHello_func_NativeHello_sig = int Function(int, Pointer<Utf8>);

// ----------LIBNATIVEHELLO----------

class libNativeHello {

    static _libNativeHello_func_NativeHello_sig? _NativeHello;

    void _initRefs() {
        if (
            _NativeHello == null
        ) {
            final lib = DynamicLibrary.open('build\\objects\\shared/native\\libNativeHello.dll');

            _NativeHello = lib.lookupFunction<_libNativeHello_func_NativeHello_native_sig, _libNativeHello_func_NativeHello_sig>('NativeHello');
        }
    }

    libNativeHello() {
        _initRefs();
    }

    int NativeHello(int arg1, String arg2) {
        return _NativeHello!(arg1, arg2.toNativeUtf8());
    }

}


