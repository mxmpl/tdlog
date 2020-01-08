import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Ouvrier } from '../ouvrier';
import { MessageService } from './message.service';


@Injectable({ providedIn: 'root' })
export class OuvrierService {

  private listeOuvriersUrl = 'http://127.0.0.1:5000/listeOuvriers/';

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  /** GET ouvriers from the server */
  getOuvriers (): Observable<Ouvrier[]> {
    return this.http.get<Ouvrier[]>(this.listeOuvriersUrl)
      .pipe(
        tap(_ => this.log('ouvriers récupérés')),
        catchError(this.handleError<Ouvrier[]>('getOuvriers', []))
      );
  }

  /** GET ouvriers by id. Return `undefined` when id not found */
  getOuvrierNo404<Data>(id: number): Observable<Ouvrier> {
    const url = `${this.listeOuvriersUrl}?id=${id}`;
    return this.http.get<Ouvrier[]>(url)
      .pipe(
        map(ouvriers => ouvriers[0]), // returns a {0|1} element array
        tap(h => {
          const outcome = h ? `récupéré` : `pas trouvé`;
          this.log(`${outcome} ouvrier id=${id}`);
        }),
        catchError(this.handleError<Ouvrier>(`getOuvrier id=${id}`))
      );
  }

  /** GET ouvrier by id. Will 404 if id not found */
  getOuvrier(id_ouvrier: number): Observable<Ouvrier> {
    const url = `${this.listeOuvriersUrl}${id_ouvrier}`;
    return this.http.get<Ouvrier>(url).pipe(
      tap(_ => this.log(`fetched ouvrier id_ouvrier=${id_ouvrier}`)),
      catchError(this.handleError<Ouvrier>(`getOuvrier id_ouvrier=${id_ouvrier}`))
    );
  }

  /* GET ouvriers whose name contains search term */
  // searchOuvriers(term: string): Observable<Ouvrier[]> {
  //   if (!term.trim()) {
  //     // if not search term, return empty ouvrier array.
  //     return of([]);
  //   }
  //   return this.http.get<Ouvrier[]>(`${this.listeOuvriersUrl}?name=${term}`).pipe(
  //     tap(_ => this.log(`found ouvriers matching "${term}"`)),
  //     catchError(this.handleError<Ouvrier[]>('searchHeroes', []))
  //   );
  // }

  //////// Save methods //////////

  /** POST: add a new ouvrier to the server */
  addOuvrier (ouvrier: Ouvrier): Observable<Ouvrier> {
    return this.http.post<Ouvrier>(this.listeOuvriersUrl, ouvrier, this.httpOptions).pipe(
      tap((newOuvrier: Ouvrier) => this.log(`ouvrier ajoute w/ id_ouvrier=${newOuvrier.id_ouvrier}`)),
      catchError(this.handleError<Ouvrier>('addOuvrier'))
    );
  }

  /** DELETE: delete the ouvrier from the server */
  deleteOuvrier (ouvrier: Ouvrier | number): Observable<Ouvrier> {
    const id = typeof ouvrier === 'number' ? ouvrier : ouvrier.id_ouvrier;
    const url = `${this.listeOuvriersUrl}${id}`;

    return this.http.delete<Ouvrier>(url, this.httpOptions).pipe(
      tap(_ => this.log(`deleted ouvrier id_ouvrier=${id}`)),
      catchError(this.handleError<Ouvrier>('deleteOuvrier'))
    );
  }

  /** PUT: update the ouvrier on the server */
  updateOuvrier (ouvrier: Ouvrier): Observable<any> {
    const id = typeof ouvrier === 'number' ? ouvrier : ouvrier.id_ouvrier;
    const url = `${this.listeOuvriersUrl}${id}`;
    return this.http.put(url, ouvrier, this.httpOptions).pipe(
      tap(_ => this.log(`updated ouvrier id_ouvrier=${ouvrier.id_ouvrier}`)),
      catchError(this.handleError<any>('updateOuvrier'))
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
