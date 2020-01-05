import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface GoogleVolumeListResponse {
  totalItems: number;
  items: Array<{
      //ouvrier:string;
        ouvrier : string;
  }>;
}

export class Ouvrier {

  ouvrier?: string;

  constructor(args: Ouvrier = {}) {
      this.ouvrier = args.ouvrier;
  }

}

@Component({
  selector: 'app-ouvriers',
  templateUrl: './ouvriers.component.html',
  styleUrls: ['./ouvriers.component.css']
})
export class OuvriersComponent implements OnInit {
  
  ouvrierCount: number;
  //bookList: Array<{ouvrier : string}>;
  ouvrierList: Ouvrier[];

  ouvrierToAdd: string;

​
  private _ouvrierListUrl = 'http://127.0.0.1:5000/listeOuvriers/';
  private _addOuvrierUrl = 'http://127.0.0.1:5000/addOuvriers/';
  //private _bookListUrl = 'https://www.googleapis.com/books/v1/volumes?q=extreme%20programming';

  constructor(private _httpClient: HttpClient) {
  }

  ngOnInit() {
      this._httpClient.get<GoogleVolumeListResponse>(this._ouvrierListUrl)
          .subscribe(googleVolumeListResponse => {

              this.ouvrierCount = googleVolumeListResponse.totalItems;​
              this.ouvrierList = googleVolumeListResponse.items.map(item => new Ouvrier({
                ouvrier: item.ouvrier
            }));
            
          })
  }

  addOuvrier(){
    this._httpClient.get<GoogleVolumeListResponse>(this._addOuvrierUrl)
    .subscribe(googleVolumeListResponse => {

      this.ouvrierCount = googleVolumeListResponse.totalItems;​
      this.ouvrierList = googleVolumeListResponse.items.map(item => new Ouvrier({
        ouvrier: item.ouvrier
    }));
    
  })
    
  }

  selectedOuvrier: Ouvrier;
  ouvriers: Ouvrier[];
  


  onSelect(ouvrier: Ouvrier): void {
  	this.selectedOuvrier = ouvrier;
  }
}


 /*
  bookCount: number;

​
  private _bookListUrl = 'https://www.googleapis.com/books/v1/volumes?q=extreme%20programming';

  constructor(private _httpClient: HttpClient) {
  }

  ngOnInit() {
      this._httpClient.get<GoogleVolumeListResponse>(this._bookListUrl)
          .subscribe(googleVolumeListResponse => {

              this.bookCount = googleVolumeListResponse.totalItems;​
             
              

          });
  }
  */

