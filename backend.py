'''
BSD 3-Clause License

Copyright (c) 2018, Sagar Shivani
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistribution of this sofware without the permission of the owner will be 
  dealt as copyright hinderence and is a punishable offence.

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
###Backend database for storing vehicle information
###still needs work and connection with gui files
import sqlite3
class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS vehicle (id INTEGER PRIMARY KEY, brand TEXT, "
                    "vno TEXT, owner TEXT, address TEXT)")
        self.conn.commit()

    def insert(self, brand, vno, owner, address):
        #the NULL parameter is for the auto-incremented id
        self.cur.execute("INSERT INTO vehicle VALUES(NULL,?,?,?,?)", (brand, vno, owner, address))
        self.conn.commit()


    def view(self):
        self.cur.execute("SELECT * FROM vehicle")
        rows = self.cur.fetchall()

        return rows

    def search(self,brand="", vno="", owner="", address=""):
        self.cur.execute("SELECT * FROM vehicle WHERE brand = ? OR vno = ? OR owner = ? "
                    "OR address = ?", (brand, vno, owner, address))
        rows = self.cur.fetchall()
        #conn.close()
        return rows

    def delete(self,id):
        self.cur.execute("DELETE FROM vehicle WHERE id = ?", (id,))
        self.conn.commit()
        #conn.close()

    def update(self,id, brand, vno, owner, address):
        self.cur.execute("UPDATE vehicle SET brand = ?, vno = ?, owner = ?, address = ? WHERE id = ?", (brand, vno, owner, address, id))
        self.conn.commit()

    #destructor-->now we close the connection to our database here
    def __del__(self):
        self.conn.close()
