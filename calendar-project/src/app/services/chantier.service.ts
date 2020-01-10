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

  private listeChantiersUrl = 'http://127.0.0.1:5000/listeOuvriers/';
  private listeOuvriersUrl = 'http://127.0.0.1:5000/listeOuvriers/';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  getChantiersDispos(id_ouvrier: number): Observable<Map<string,Chantier[]>> {
  	const url = `${this.listeOuvriersUrl}${id_ouvrier}/chantiersdispos`;
    return this.http.get<Map<string,Chantier[]>>(url)
      .pipe(
        tap(_ => this.log('chantiers dispos récupérés')),
        catchError(this.handleError<Map<string,Chantier[]>>('getChantiersDispos'))
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
