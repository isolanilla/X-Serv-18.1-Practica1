#!/usr/bin/python


"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp


class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    content = {}
    contador = 0

    def formulario(self):
        return ( "<form method='post'>FORMUMLARIO URLS ACORTADAS:<input type='text'name='valor' value='' /><button type='submit'> Enviar</button></form>")

    def printcontent(self):
        codehtml = ""
        urlink1 = ""
        urlink2 = ""
        for key in  self.content.keys():
            urlink1  = "<a href='http://localhost:1234/"+ str(key) +  "'>"+ "http://localhost:1234/"+str(key) + "</a>"
            urlink2 = "<a href='"+ str(self.content[int(key)]) +  "'>"+ str(self.content[int(key)]) + "</a>"
            codehtml = codehtml +  "<p>Pagina: " + str(urlink2) +"----URCL acortada----->"+ str(urlink1) +"</p>"


        return codehtml

    def parse(self, request):
        """Return the resource name (including /)"""

        recurso = request.split(' ',2)[1]
        metodo = request.split(' ',2)[0]
        
        if metodo == "POST":
            cuerpo = request.split("\r\n\r\n",1)[1]
        else:
            cuerpo = ""


        return (metodo, recurso, cuerpo)

    def process(self, resourceName):


        metodo, recurso, cuerpo = resourceName
        httpCode = ""
        htmlBody =""
        cuerpoencontrado = False


        if metodo == "GET":
            if recurso == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body>" +  self.formulario() + self.printcontent() + "</body></html>"
            else:
                recurso = recurso.split("/",1)[1]
                if (int(recurso) < self.contador):
                    pagina = self.content[int(recurso)]
                    httpCode = "307 REDIRECT"
                    htmlBody = '<html><body><h1>WAIT REDIRECT....</h1><meta http-equiv="Refresh" content="2;url='+ str(pagina) +'"></body></html>'
                else: 
                     httpCode = "404 NOT FOUND"                
                     htmlBody = "<html><body><h1>PAGINA NO ENCONTRADA </h1><p><a href='http://localhost:1234'>formulario</a></p></body></html>"



        if metodo == "POST":

            cuerpo = cuerpo.split('=')[1]

            if cuerpo.find("http%3A%2F%2F") >=  0:
                cuerpo = cuerpo.split('http%3A%2F%2F')[1]

            cuerpo = "http://" + cuerpo

            for key  in self.content.keys():
                if (self.content[key] == cuerpo):
                    cuerpoencontrado = True
                    break

            if not cuerpoencontrado:
                self.content[self.contador] = cuerpo
                self.contador += 1


            for  key in  self.content.keys():
                if (cuerpo == self.content[int(key)]):
                    numero = key


            urlink1 = "<a href='http://localhost:1234/" + str(numero) +  "'>" + "http://localhost:1234/"+ str(numero) + "</a>"
            urlink2 = "<a href='" + str(cuerpo) +  "'>" + str(cuerpo)+ "</a>"
            urlink3 = "<a href='http://localhost:1234'>formulario</a>"
                           

            httpCode = "200 OK"
            htmlBody ="<html><body><h1>URL acortada: " + str(cuerpo) + "</h1> Enlaces: <p>" + str(urlink3) +"</p><p>"+ str(urlink2) +"</p><p>" + str(urlink1) + "</p><html><body>"


        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
