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


