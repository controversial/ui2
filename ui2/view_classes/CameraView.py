import ctypes

import objc_util
import ui


AVCaptureSession = objc_util.ObjCClass("AVCaptureSession")
AVCaptureDevice = objc_util.ObjCClass("AVCaptureDevice")
AVCaptureDeviceInput = objc_util.ObjCClass("AVCaptureDeviceInput")
AVCaptureVideoPreviewLayer = objc_util.ObjCClass("AVCaptureVideoPreviewLayer")


class UnsupportedDeviceError(Exception):
    """Raised if your iOS device isn't supported."""
    pass


class CameraView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._objc = objc_util.ObjCInstance(self)

        # Set up the camera device
        self._session = AVCaptureSession.new()
        camera_type = ctypes.c_void_p.in_dll(objc_util.c, "AVMediaTypeVideo")
        device = AVCaptureDevice.defaultDeviceWithMediaType(camera_type)
        input = AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
        if input:
            self._session.addInput(input)
        else:
            raise UnsupportedDeviceError("Failed to connect to camera.")

        # Add the camera preview layer
        self._layer = self._objc.layer()
        self._camera_layer = AVCaptureVideoPreviewLayer.layerWithSession(
            self._session
        )
        self._layer.addSublayer(self._camera_layer)

        self._auto_rotating = True

    @ui.in_background  # Apple recommends this at http://apple.co/2a1Ayca
    def start(self):
        """Start the capture."""
        self._session.startRunning()

    def stop(self):
        """Stop the capture."""
        self._session.stopRunning()

    @property
    def running(self):
        return self._session.running()

    def layout(self):
        """Called when the view's size changes to resize the layer."""
        self._camera_layer.setFrame(((0, 0), (self.width, self.height)))
