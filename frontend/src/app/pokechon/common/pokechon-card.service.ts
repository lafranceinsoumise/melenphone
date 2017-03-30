import { Injectable } from '@angular/core';
import { PokechonCardInfo } from './pokechon-card-info';

const POKECHON_CARD_INFO_MOCK: PokechonCardInfo[] = [
  {
    id: 'lkjlzaknfazf',
    pokechon: {
      id: 'nzflknflkzan',
      name: 'Lézarkozy',
      realName: 'Nicolas Sarkozy',
      descriptionText: [
        'Et pis çuilà qui porte le burkini, j’y coupe les allocs !.',
        'La république, c’est les frites !’',
        'La france a toujours été du côté des dictateurs',
        'Vous avez vu ma femme ? Elle est belle, hein ?'
      ],
    }
  },
  {
    id: 'mdljalmdjazmln',
    pictureSource: 'kaijuppe.jpg',
    pokechon: {
      id: 'dlkazkdnzl',
      name: 'Kaijuppé',
      realName: 'Alain Juppé',
      descriptionText: [
        'Le meilleur d’entre nous.'
      ]
    }
  },
  {
    id: 'kdjzatjra',
    pictureSource: 'fionfion.jpg',
    pokechon: {
      id: 'ladzlamlnda',
      name: 'Fionfion',
      realName: 'François Fillon',
      descriptionText: [
        'Mais puisque j’vous dis que Pénélope n’a rien fait !',
        'Péné, tu sais où j’ai pu foutre les clés du Falcon ?'
      ]
    }
  }
];

@Injectable()
export class PokechonCardService {

  constructor() { }

  getPokechonCards(): Promise<PokechonCardInfo[]> {
    return Promise.resolve(POKECHON_CARD_INFO_MOCK);
  }

}
