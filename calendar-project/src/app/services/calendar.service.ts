import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// import { Chantier } from '../Chantier';

@Injectable({
  providedIn: 'root'
})

export class CalendarService {
  constructor(private http:HttpClient){}
  chantiersUrl : string = "http://127.0.0.1:5000/listeChantiers/";
  getData():Observable<any[]>{
  	return this.http.get<any[]>(this.chantiersUrl);
  }
}
