#! /usr/bin/python
#    Author:  Arjun Sarwal   arjun@laptop.org
#    Copyright (C) 2007, OLPC
#    
#    	
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import signal, os
import time
import audioop
import subprocess
from struct import *
from string import *
from numpy.oldnumeric import *
from numpy.fft import *
import alsaaudio
from alsaaudio import Mixer

class AudioGrab():

    def __init__(self):
        
        self.rate=4000                                              #Default sampling rate at startup of device
        self.handoff_state = True
        
        self.sensor_type = 0
        self.sensor_val1 = -1
        
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setchannels(1)
        self.inp.setperiodsize(160)

        # test to see if DC Mode is enabled 
        try:
            self.dcmode = Mixer('DC Mode Enable')
            self.bias = Mixer('V_REFOUT Enable')
            self.has_dcmode = True
        except:
            print "DC Mode unavailable"
            self.has_dcmode = False

    def _final_calculate_sensor_val(self, raw_buffer):
        """This function is used to compute the sensor value to be returned from the raw buffer value"""
        sensor_val1  = 0
        buf = str(raw_buffer)
        if self.sensor_type ==1 :
            integer_buffer = list(unpack( str(int(len(buf))/2)+'h' , buf))
            integer_buffer = integer_buffer[0:128]
            fftx = real_fft(integer_buffer, 128,-1)
            fftx=fftx[10:len(fftx)]
            buffers=[abs(y) for y in fftx]
            max_val1=10
            max_buffers = max(buffers)
            for x in range(0,len(buffers)):
                if buffers[x]==max_buffers:
                    max_val1=x
            sensor_val1= (max_val1*1.75)
            if sensor_val1>=100:
                sensor_val1=100
                #(above)mapping values from 40 to 120 to values 0-100 as index 40 to 120 were found most responsive to voice and whistle
                
        #elif self.sensor_type == 1:
        #    sensor_val1 =  (audioop.rms(buf, 2)*0.0030466)
        elif self.sensor_type==0:
            sensor_val1 = (audioop.rms(buf, 2)*0.0030466)
        elif self.sensor_type==2:
            sensor_val1 = (audioop.avg(buf, 2)*0.00152333) + 50.0
        elif self.sensor_type==3:
            sensor_val1 =  (audioop.rms(buf, 2)*0.0030466)
                
        sensor_val1=(sensor_val1*3.0)       #To return a value between 0 and 300 
        return sensor_val1
        
    def get_sensor_val(self, sensor_type = 0):
        """Calculates sensor value based upon appropriate mode and puts it in the queue"""
        data_buffer = self.read_samples(sensor_type)
        final_sensor_val  = self._final_calculate_sensor_val(data_buffer)
        return final_sensor_val
    
    def read_samples(self, sensor_type =0):
        self.set_sensor_type(sensor_type)
        l,data = self.inp.read()
        return data
    
    def mute_master(self):
        """Mutes the Master Control"""
        os.system("amixer set Master mute")
    
    def unmute_master(self):
        """Unmutes the Master Control"""
        os.system("amixer set Master unmute")
    
    def mute_PCM(self):
        """Mutes the PCM Control"""
        os.system("amixer set PCM mute")
    
    def unmute_PCM(self):
        """Unmutes the PCM Control"""
        os.system("amixer set PCM unmute")
    
    def mute_mic(self):
        """Mutes the Mic Control"""
        os.system("amixer set Mic mute")
    
    def unmute_mic(self):
        """Unmutes the Mic Control"""
        os.system("amixer set Mic unmute")
    
    def set_master(self, master_val ):
        """Sets the Master gain slider settings 
        master_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set"""
        os.system("amixer set Master " + str(master_val) + "%")
        
    def get_master(self):
        """Gets the Master gain slider settings. The value returned is an integer between 0-100
        and is an indicative of the percentage 0 - 100%"""
        p = str(subprocess.Popen(["amixer", "get", "Master"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Front Left:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"%]")]
        return int(p)
    
    def get_mix_for_recording(self):
        """Returns True if Mix is set as recording device and False if it isn't """
        p = str(subprocess.Popen(["amixer", "get", "Mix", "capture", "cap"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Mono:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"]")]
        if p=="on" :
            return True
        else:
            return False

    def get_mic_for_recording(self):
        """Returns True if mic is set as recording device and False if it isn't """
        p = str(subprocess.Popen(["amixer", "get", "Mic", "capture", "cap"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Mono:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"]")]
        if p=="on" :
            return True
        else:
            return False
    
    def set_mic_for_recording(self):
        """Sets Mic as the default recording source"""
        os.system("amixer set Mic capture cap")
    
    def set_mix_for_recording(self):
        """Sets Mix as the default recording source"""
        os.system("amixer set Mix capture cap")
    
    def set_bias(self,bias_state=False):
        """Sets the Bias control
        pass False to disable and True to enable"""
        if self.has_dcmode:
            if bias_state==False:
                self.bias.setmute(1)
            else:
                self.bias.setmute(0)
   
    def get_bias(self):
        """Returns the setting of Bias control 
        i.e. True: Enabled and False: Disabled"""
        if self.has_dcmode:
            p = str(subprocess.Popen(["amixer", "get", "'V_REFOUT Enable'"], stdout=subprocess.PIPE).communicate()[0])
            p = p[find(p,"Mono:"):]
            p = p[find(p,"[")+1:]
            p = p[:find(p,"]")]
            if p=="on" :
                return True
            else:
                return False
        else: return False
   
    def set_dc_mode(self, dc_mode = False):
        """Sets the DC Mode Enable control
        pass False to mute and True to unmute"""
        if self.has_dcmode:
            if dc_mode==False:
                self.dcmode.setmute(1)
            else:
                self.dcmode.setmute(0)

    def get_dc_mode(self):
        """Returns the setting of DC Mode Enable control 
        i .e. True: Unmuted and False: Muted"""
        if self.has_dcmode:
            p = str(subprocess.Popen(["amixer", "get", "'DC Mode Enable'"], stdout=subprocess.PIPE).communicate()[0])
            p = p[find(p,"Mono:"):]
            p = p[find(p,"[")+1:]
            p = p[:find(p,"]")]
            if p=="on" :
                return True
            else:
                return False
        else: return False
        
    def set_mic_boost(self, mic_boost=False):
        """Sets the Mic Boost +20dB control
        pass False to mute and True to unmute"""
        if mic_boost==False:
            mb_str="mute"
        else:
            mb_str="unmute"
        os.system("amixer set 'Mic Boost (+20dB)' " + mb_str)
        
    def get_mic_boost(self):
        """Returns the setting of Mic Boost +20dB control 
        i.e. True: Unmuted and False: Muted"""
        p = str(subprocess.Popen(["amixer", "get", "'Mic Boost (+20dB)'"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Mono:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"]")]
        if p=="on" :
            return True
        else:
            return False
            
    def set_capture_gain(self, capture_val):
        """Sets the Capture gain slider settings 
        capture_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set"""
        os.system("amixer set Capture " + str(capture_val) + "%")
        
    def get_capture_gain(self):
        """Gets the Capture gain slider settings. The value returned is an integer between 0-100
        and is an indicative of the percentage 0 - 100%"""
        p = str(subprocess.Popen(["amixer", "get", "Capture"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Front Left:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"%]")]
        return int(p)
        
    def set_PCM_gain(self, PCM_val):
        """Sets the PCM gain slider settings 
        PCM_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set"""
        os.system("amixer set PCM " + str(PCM_val) + "%")
        
    def get_PCM_gain(self):
        """Gets the PCM gain slider settings. The value returned is an indicative of the percentage 0 - 100%"""
        p = str(subprocess.Popen(["amixer", "get", "PCM"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Front Left:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"%]")]
        return int(p)
        
    def set_mic_gain(self, mic_val):
        """Sets the MIC gain slider settings 
        mic_val must be given as an integer between 0 and 100 indicating the
        percentage of the slider to be set"""
        os.system("amixer set Mic " + str(mic_val) + "%")
        
    def get_mic_gain(self):
        """Gets the MIC gain slider settings. The value returned is an indicative of the percentage 0 - 100%"""
        p = str(subprocess.Popen(["amixer", "get", "Mic"], stdout=subprocess.PIPE).communicate()[0])
        p = p[find(p,"Mono:"):]
        p = p[find(p,"[")+1:]
        p = p[:find(p,"%]")]
        return int(p)
    
    def set_sampling_rate(self, sr):
        """Sets the sampling rate of the capture device
        Sampling rate must be given as an integer for example 16000 for setting 16Khz sampling rate
        The sampling rate would be set in the device to the nearest available"""
        caps_str = "audio/x-raw-int,rate=%d,channels=1,depth=16" % (sr, )
        self.caps1.set_property("caps", gst.caps_from_string(caps_str) )

    def get_sampling_rate(self):
        """Gets the sampling rate of the capture device"""
        return int(self.caps1.get_property("caps")[0]['rate'] )

    def set_callable1(self, callable1):
        """Sets the callable to the drawing function for giving the
        data at the end of idle-add"""
        self.callable1 = callable1
        
    def save_settings(self):
        """Save audio device settings at startup"""
    
    def save_settings_temp(self):
        """Save settings temporarily. For example if activity is going to be inactive for some time"""
    
    def apply_settings_temp(self):
        """Re-apply settings that were saved temporarily. For example Activity becomes active again"""
    
    def apply_settings(self):
        """Apply settings that were saved at the beginning. Ideally should be called on quitting, and after pipeline has been stopped"""

    def set_sensor_type(self, sensor_type=1):
        """Set the type of sensor you want to use. Set sensor_type according to the following
        0 - AC coupling with Bias On --> The default settings. The internal MIC uses these
        1 - AC coupling with Bias On , FFT mode --> slightly more gain than type (1), FFTs are calculated in this mode
        2 - DC coupling with Bias On --> Used with resistive sensors. For example an LDR, NTC
        3 - DC coupling with Bias Off --> Used when using a voltage output sensor. For example LM35 which gives output proportional to temperature"""
        if sensor_type==0:
            self.set_dc_mode(False)
            self.set_bias(True)
            self.set_capture_gain(40)
            self.set_mic_boost(True)
        elif sensor_type==1:
            self.set_dc_mode(False)
            self.set_bias(True)
            self.set_capture_gain(70)
            self.set_mic_boost(True)
        elif sensor_type==2:
            self.set_dc_mode(True)
            self.set_bias(True)
            self.set_capture_gain(0)
            self.set_mic_boost(False)
        elif sensor_type==3:
            self.set_dc_mode(True)
            self.set_bias(False)
            self.set_capture_gain(0)
            self.set_mic_boost(False)
            
        self.sensor_type = sensor_type
        
    
