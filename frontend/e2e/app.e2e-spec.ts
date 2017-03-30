import { JlmPBPage } from './app.po';

describe('jlm-pb App', function() {
  let page: JlmPBPage;

  beforeEach(() => {
    page = new JlmPBPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('jlm works!');
  });
});
