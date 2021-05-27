const changeForm = () => {
  const type = $('#type').text();

  const form_investor = $('#investor-form');
  const form_peminjam = $('#peminjam-form');

  if (type === 'Investor') {
    $('#type').text('Peminjam');
    form_investor.hide();
    form_peminjam.show();
  } else {
    $('#type').text('Investor');
    form_investor.show();
    form_peminjam.hide();
  }
};
