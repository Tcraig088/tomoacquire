import enum
import tomobase 
from tomoacquire.napari.layer_widgets.scanwindow import ScanWindowDataWidget
from tomobase import TOMOBASE_DATATYPES

TOMOBASE_DATATYPES.append(SCANWINDOW=ScanWindowDataWidget)

class ScanWindow(tomobase.data.Image):
    def __init__(self, data, pixelsize=1.0):
        super().__init__(data, pixelsize)

        self.dosage = 0.0
        self.images_acquired = 0
        self.angle = 0.0
        self.magnification = 1.0
        self.time_start = 0.0
        self.time_current = 0.0

    def _to_napari_layer(self, astuple = True ,**kwargs):
        layer_info = {}
        
        layer_info['name'] = kwargs.get('name', 'ScanWindow')
        layer_info['scale'] = kwargs.get('pixelsize' ,(self.pixelsize, self.pixelsize, self.pixelsize))
        metadata = {'type': TOMOBASE_DATATYPES.SCANWINDOW.value(),
                    'dosage': self.dosage,
                    'images_acquired': self.images_acquired,
                    'angle': self.angle,
                    'magnification': self.magnification,
                    'times': (self.time_start, self.time_current)}	
        
        if 'viewsettings' in kwargs:
            for key, value in kwargs['viewsettings'].items():
                layer_info[key] = value
            
        for key, value in kwargs.items():
            if key != 'name' and key != 'pixelsize' and key != 'viewsettings':
                metadata[key] = value
                
        if len(self.data.shape) == 2:
            self.data = self.data.transpose(0,1)
            metadata['axis_labels'] = ['y', 'x']
        elif len(self.data.shape) == 3:
            self.data = self.data.transpose(2,0,1)
            metadata['axis_labels'] = ['Signals', 'y', 'x']
            
        layer = (self.data, layer_info ,'image')
        layer_info['metadata'] = {'ct metadata': metadata}
        
        if astuple:
            return layer
        else:
            import napari
            return napari.layers.Layer.create(*layer)
    
    @classmethod
    def _from_napari_layer(cls, layer):
        if layer.metadata['ct metadata']['type'] != TOMOBASE_DATATYPES.SCANWINDOW.value():
            raise ValueError(f'Layer of type {layer.metadata["ct metadata"]["type"]} not recognized')
        
        if len(layer.data.shape) == 2:
            pass
        elif len(layer.data.shape) == 3:
            data = layer.data.transpose(1, 2, 0)
        sinogram = ScanWindow(data, layer.metadata['ct metadata']['angles'], layer.scale[0])
        return sinogram
