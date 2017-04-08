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
    public basic: BasicService
  ) {}

  ngOnInit() {
  }

  makeBackendRequest() {
    if (!isDevMode()) return;
    this.http.post('/api/simulate_call', '')
      .toPromise()
      .then((res: Response) => {
        if (res.status !== 200) {
          throw new Error(`erreur de communication avec le serveur : ${res.status}`);
        }
      })
      .catch(error => console.error(error));
  }
}
