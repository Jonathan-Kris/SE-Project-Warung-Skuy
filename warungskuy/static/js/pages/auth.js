const changeForm = () => {
  const type = $('#type').text();

  const form_investor = $('#investor-form');
  const form_peminjam = $('#peminjam-form');

  if (type === 'Lender') {
    $('#type').text('Borrower');
    form_investor.hide();
    form_peminjam.show();
    localStorage.setItem('register', 'borrower');
    console.log(localStorage.getItem('register'));
  } else {
    $('#type').text('Lender');
    form_investor.show();
    form_peminjam.hide();
    localStorage.setItem('register', 'lender');
    console.log(localStorage.getItem('register'));
  }
};

$(() => {
  const type = $('#type').text();

  const form_investor = $('#investor-form');
  const form_peminjam = $('#peminjam-form');

  if (localStorage.getItem('register') == 'lender') {
    $('#type').text('Lender');
    form_investor.show();
    form_peminjam.hide();
  } else if (localStorage.getItem('register') == 'borrower') {
    $('#type').text('Borrower');
    form_investor.hide();
    form_peminjam.show();
  }
});
