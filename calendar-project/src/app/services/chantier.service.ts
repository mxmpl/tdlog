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
  private listeChantiersHorairesUrl = 'http://127.0.0.1:5000/listeChantiers/horaires'

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }


  /** GET chantiers from the server */
  getChantiers (): Observable<Chantier[]> {
    return this.http.get<Chantier[]>(this.listeChantiersUrl)
      .pipe(
        tap(_ => this.log('chantiers récupérés')),
        catchError(this.handleError<Chantier[]>('getChantiers', []))
      );
  }

  /** GET chantier by name. Will 404 if id not found */
  getChantier(name_chantier: string): Observable<Chantier> {
    const url = `${this.listeChantiersUrl}${name_chantier}`;
    return this.http.get<Chantier>(url).pipe(
      tap(_ => this.log(`fetched chantier name_chantier=${name_chantier}`)),
      catchError(this.handleError<Chantier>(`getChantier name_chantier=${name_chantier}`))
    );
  }

/*   GET chantier by id. Will 404 if id not found 
  getChantierHoraire(id_chantier: number): Observable<Chantier> {
    const url = `${this.listeChantiersHorairesUrl}${id_chantier}`;
    return this.http.get<Chantier>(url).pipe(
      tap(_ => this.log(`fetched chantier name_chantier=${id_chantier}`)),
      catchError(this.handleError<Chantier>(`getChantier name_chantier=${id_chantier}`))
    );
  } */

  getChantiersDispos(id_ouvrier: number): Observable<Map<string,Chantier[]>> {
  	const url = `${this.listeOuvriersUrl}${id_ouvrier}/chantiersdispos`;
    return this.http.get<Map<string,Chantier[]>>(url)
      .pipe(
        tap(_ => this.log('chantiers dispos récupérés')),
        catchError(this.handleError<Map<string,Chantier[]>>('getChantiersDispos'))
      );
  }

  /** POST: add a new chantier to the server */
  addChantier (chantier: Chantier): Observable<Chantier> {
    return this.http.post<Chantier>(this.listeChantiersUrl, chantier, this.httpOptions).pipe(
      tap((newChantier: Chantier) => this.log(`chantier ajoute`)),//, w/ id_chantier=${newChantier.id_chantier}`)),
      catchError(this.handleError<Chantier>('addChantier'))
    );
  }

  /** DELETE: delete the chantier from the server */
   deleteChantier (chantier: Chantier | string): Observable<Chantier> {
    const name = typeof chantier === 'string' ? chantier : chantier.name_chantier;
    const url = `${this.listeChantiersUrl}${name}`;

    return this.http.delete<Chantier>(url, this.httpOptions).pipe(
      tap(_ => this.log(`deleted chantier name_chantier=${name}`)),
      catchError(this.handleError<Chantier>('deleteChantier'))
    );
  } 

  addAttributions(ouvrier: Ouvrier, chantiers_choisis: Chantier[]): Observable<Ouvrier> {
    var couples = [];
    for (var i=0; i<chantiers_choisis.length; i++){
      couples.push({"id_ouvrier":ouvrier.id_ouvrier, "id_chantier":chantiers_choisis[i].id_chantier})
    }
    return this.http.post<Ouvrier>(this.attributionUrl, couples, this.httpOptions).pipe(
        tap((newOuvrier: Ouvrier) => this.log(`attributions ajoutes`)),
        catchError(this.handleError<Ouvrier>('addAttribution'))
      );
  }

  deleteAttribution(ouvrier: Ouvrier, chantier: Chantier) {
    const url = `${this.attributionUrl}${ouvrier.id_ouvrier}/${chantier.id_chantier}`;
    return this.http.delete<Ouvrier>(url, this.httpOptions).pipe(
      tap((newOuvrier: Ouvrier) => this.log(`attribution supprime`)),
      catchError(this.handleError<Ouvrier>('deleteAttribution'))
    );
  }


    /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /** Log a OuvrierService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`OuvrierService: ${message}`);
  }
}
