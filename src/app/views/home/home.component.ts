import { Component, OnInit, isDevMode } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { BasicService } from '../../shared';

@Component({
  selector: 'jlm-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  get isDevMode() {
    return isDevMode();
  }

  constructor(
    private http: Http,
    private basic: BasicService
  ) {}

  ngOnInit() {
  }

  makeBackendRequest() {
    this.http.post('/api/simulate_call', '')
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error(`erreur de communication avec le serveur : ${res.status}`);
        }
        return res.json();
      })
      .catch(error => console.error(error));
  }
}
