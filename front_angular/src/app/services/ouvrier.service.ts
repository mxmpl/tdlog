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

  /** GET les ouvriers du serveur */
  getOuvriers (): Observable<Ouvrier[]> {
    return this.http.get<Ouvrier[]>(this.listeOuvriersUrl)
      .pipe(
        catchError(this.handleError<Ouvrier[]>('getOuvriers', []))
      );
  }

  /** GET ouvrier par id */
  getOuvrier(id_ouvrier: number): Observable<Ouvrier> {
    const url = `${this.listeOuvriersUrl}${id_ouvrier}`;
    return this.http.get<Ouvrier>(url).pipe(
      catchError(this.handleError<Ouvrier>(`getOuvrier id_ouvrier=${id_ouvrier}`))
    );
  }

  /** POST: ajoute un nouvel ouvrier au serveur */
  addOuvrier (ouvrier: Ouvrier): Observable<Ouvrier> {
    return this.http.post<Ouvrier>(this.listeOuvriersUrl, ouvrier, this.httpOptions).pipe(
      catchError(this.handleError<Ouvrier>('addOuvrier'))
    );
  }

  /** DELETE: supprime un ouvrier du serveur */
  deleteOuvrier (ouvrier: Ouvrier | number): Observable<Ouvrier> {
    const id = typeof ouvrier === 'number' ? ouvrier : ouvrier.id_ouvrier;
    const url = `${this.listeOuvriersUrl}${id}`;

    return this.http.delete<Ouvrier>(url, this.httpOptions).pipe(
      catchError(this.handleError<Ouvrier>('deleteOuvrier'))
    );
  }

  /** PUT: met a jour l'ouvrier sur le serveur */
  updateOuvrier (ouvrier: Ouvrier): Observable<any> {
    const id = typeof ouvrier === 'number' ? ouvrier : ouvrier.id_ouvrier;
    const url = `${this.listeOuvriersUrl}${id}`;
    return this.http.put(url, ouvrier, this.httpOptions).pipe(
      catchError(this.handleError<any>('updateOuvrier'))
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
