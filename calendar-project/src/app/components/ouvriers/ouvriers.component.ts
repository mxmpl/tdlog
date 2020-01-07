import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface GoogleVolumeListResponse {
 // totalItems: number;
  items: Array<{
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
  
  //ouvrierCount: number;
  //bookList: Array<{ouvrier : string}>;
  ouvrierList: Ouvrier[];

  ouvrierToAdd: string;

​
  private _ouvrierListUrl = 'http://127.0.0.1:5000/listeOuvriers/';
  private _addOuvrierUrl = 'http://127.0.0.1:5000/addOuvriers/';

  constructor(private http: HttpClient) {
  }

  ngOnInit() {
      this.http.get<GoogleVolumeListResponse>(this._ouvrierListUrl)
          .subscribe(googleVolumeListResponse => {

              //this.ouvrierCount = googleVolumeListResponse.totalItems;​
              this.ouvrierList = googleVolumeListResponse.items.map(item => new Ouvrier({
                ouvrier: item.ouvrier
            }));
            
          })
  }

  addOuvrier(obj){
    console.log(obj)
    this.http.post(this._addOuvrierUrl, {"nom":obj}, {})
    .subscribe(data  => {console.log("PUT Request is successful ", data);},
               error  => {console.log("Error", error);});
  }

  deleteOuvrier(obj){}

  addAff(obj){
    this.addOuvrier(obj)
    this.ngOnInit();
  }

  selectedOuvrier: Ouvrier;
  ouvriers: Ouvrier[];
  


  onSelect(ouvrier: Ouvrier): void {
  	this.selectedOuvrier = ouvrier;
  }
}
