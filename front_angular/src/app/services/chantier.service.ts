import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Ouvrier } from '../ouvrier';
import { Chantier } from '../chantier';
import { MessageService } from './message.service';


@Injectable({
  providedIn: 'root'
})
export class ChantierService {

  private attributionUrl = 'http://127.0.0.1:5000/attribution/';
  private listeOuvriersUrl = 'http://127.0.0.1:5000/listeOuvriers/';
  private listeChantiersUrl = 'http://127.0.0.1:5000/listeChantiers/';
  
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  /** GET les chantiers du serveur */
  getChantiers (): Observable<Chantier[]> {
    return this.http.get<Chantier[]>(this.listeChantiersUrl)
      .pipe(
        catchError(this.handleError<Chantier[]>('getChantiers', []))
      );
  }

  /** GET un chantier suivant le nom */
  getChantier(name_chantier: string): Observable<Chantier> {
    const url = `${this.listeChantiersUrl}${name_chantier}`;
    return this.http.get<Chantier>(url).pipe(
      catchError(this.handleError<Chantier>(`getChantier name_chantier=${name_chantier}`))
    );
  }

  /** GET les chantiers ou un ouvrier d'identifiant donne est disponible du serveur */
  getChantiersDispos(id_ouvrier: number): Observable<Map<string,Chantier[]>> {
  	const url = `${this.listeOuvriersUrl}${id_ouvrier}/chantiersdispos`;
    return this.http.get<Map<string,Chantier[]>>(url)
      .pipe(
        catchError(this.handleError<Map<string,Chantier[]>>('getChantiersDispos'))
      );
  }

  /** POST: ajoute un chantier au serveur */
  addChantier (chantier: Chantier): Observable<Chantier> {
    return this.http.post<Chantier>(this.listeChantiersUrl, chantier, this.httpOptions).pipe(
      catchError(this.handleError<Chantier>('addChantier'))
    );
  }

  /** DELETE: supprime un chantier du serveur */
  deleteChantier (chantier: Chantier | string): Observable<Chantier> {
    const name = typeof chantier === 'string' ? chantier : chantier.name_chantier;
    const url = `${this.listeChantiersUrl}${name}`;

    return this.http.delete<Chantier>(url, this.httpOptions).pipe(
      catchError(this.handleError<Chantier>('deleteChantier'))
    );
  } 

  /** POST: ajoute des nouvelles attributions au serveur */
  addAttributions(ouvrier: Ouvrier, chantiers_choisis: Chantier[]): Observable<Ouvrier> {
    var couples = [];
    for (var i=0; i<chantiers_choisis.length; i++){
      couples.push({"id_ouvrier":ouvrier.id_ouvrier, "id_chantier":chantiers_choisis[i].id_chantier})
    }
    return this.http.post<Ouvrier>(this.attributionUrl, couples, this.httpOptions).pipe(
        catchError(this.handleError<Ouvrier>('addAttribution'))
      );
  }

  /** DELETE: supprime une attribution du serveur */
  deleteAttribution(ouvrier: Ouvrier, chantier: Chantier) {
    const url = `${this.attributionUrl}${ouvrier.id_ouvrier}/${chantier.id_chantier}`;
    return this.http.delete<Ouvrier>(url, this.httpOptions).pipe(
      catchError(this.handleError<Ouvrier>('deleteAttribution'))
    );
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      this.log(`${operation} failed: ${error.error}`);
      return of(result as T);
    };
  }

  private log(message: string) {
    this.messageService.add(`OuvrierService: ${message}`);
  }
}
