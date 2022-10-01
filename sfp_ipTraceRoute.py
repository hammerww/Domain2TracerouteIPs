# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_ipTraceRoute
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      Willy Vasquez <w.vasquezbarzola@gmail.com>
#
# Created:     04/09/2022
# Copyright:   (c) Willy Franz Vasquez Barzola 2022
# Licence:     GPL
# -------------------------------------------------------------------------------


from spiderfoot import SpiderFootEvent, SpiderFootPlugin
import subprocess
from subprocess import Popen

class sfp_ipTraceRoute(SpiderFootPlugin):

    meta = {
        'name': "IpsTraceRoute",
        'summary': "Muestra las IPs de salto para llegar a un determinado dominio",
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["DOMAIN_NAME"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["IP_ADDRESS"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")
        cadena = ""
        try:

            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            ########################
            # Insert here the code #
            ########################

            #establecer la clave del usuario linux
            password = "kali"

            p = subprocess.Popen(["sudo","-S", "traceroute", "-T", eventData], stdin = subprocess.PIPE, stdout = subprocess.PIPE)

            #envia password
            a = p.communicate((password + "\n").encode())
            a = str(a)
            a = a[1:-1]

            #DIVIDO RESULTADO POR SALTO DE LINEA
            n_data = a.split('(')

                
            #OBTENGO LA EL VALOR GUARDADO ENTRE ()
            
            for ip in n_data:
                if ')' in ip:
                    if "traceroute" not in ip:
                        ip = ip.split(')')
                        ip = ip[0]
                        cadena = cadena + ip +"\n"
            cadena = cadena.split('\n')


            if not cadena:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return


        #INGRESO LOS RESULTADOS
        for ip_v in cadena:
            evt = SpiderFootEvent("IP_ADDRESS", ip_v, self.__name__, event)
            self.notifyListeners(evt)

# End of sfp_ipTraceRoute class