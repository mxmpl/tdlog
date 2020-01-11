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

  private nouvelleAttributionUrl = 'http://127.0.0.1:5000/attribution/';
  private listeOuvriersUrl = 'http://127.0.0.1:5000/listeOuvriers/';
  private listeChantiersUrl = 'http://127.0.0.1:5000/listeChantiers/'

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

  /** GET chantier by id. Will 404 if id not found */
  getChantier(id_chantier: number): Observable<Chantier> {
    const url = `${this.listeChantiersUrl}${id_chantier}`;
    return this.http.get<Chantier>(url).pipe(
      tap(_ => this.log(`fetched chantier id_chantier=${id_chantier}`)),
      catchError(this.handleError<Chantier>(`getChantier id_chantier=${id_chantier}`))
    );
  }

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
/*   deleteChantier (chantier: Chantier | number): Observable<Chantier> {
    const id = typeof chantier === 'number' ? chantier : chantier.id_chantier;
    const url = `${this.listeChantiersUrl}${id}`;

    return this.http.delete<Chantier>(url, this.httpOptions).pipe(
      tap(_ => this.log(`deleted chantier id_chantier=${id}`)),
      catchError(this.handleError<Chantier>('deleteChantier'))
    );
  } */

  addAttribution(ouvrier: Ouvrier, chantier: Chantier): Observable<Ouvrier>  {
    const id_ouvrier = ouvrier.id_ouvrier;
    const id_chantier = chantier.id_chantier;
    return this.http.post<Ouvrier>(this.nouvelleAttributionUrl, {id_ouvrier, id_chantier}, this.httpOptions).pipe(
      tap((newOuvrier: Ouvrier) => this.log(`attribution ajoute`)),//, w/ id_ouvrier=${newOuvrier.id_ouvrier}`)),
      catchError(this.handleError<Ouvrier>('addAttribution'))
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
