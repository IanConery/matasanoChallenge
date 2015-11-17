var hexHash = {
  '0' : '0000',
  '1' : '0001',
  '2' : '0010',
  '3' : '0011',
  '4' : '0100',
  '5' : '0101',
  '6' : '0110',
  '7' : '0111',
  '8' : '1000',
  '9' : '1001',
  'a' : '1010',
  'b' : '1011',
  'c' : '1100',
  'd' : '1101',
  'e' : '1110',
  'f' : '1111'
};

var hexToBinary = function(string){
  var result = '';
  for(var i = 0; i < string.length; i++){
    result += hexHash[string[i]];
  }
  return result;
}


var fixedXOR = function(buff1, buff2){
  var bin1 = hexToBinary(buff1);
  var bin2 = hexToBinary(buff2);
  var xored = '';
  var result = '';

  for(var i = 0; i < bin1.length; i++){
    xored += bin1[i] ^ bin2[i];
    console.log(xored);
  }
  xored = xored.split('');
  while(xored.length >= 4){
    var temp = xored.splice(0,4).join('');
    for(var key in hexHash){
      if(temp === hexHash[key]){
        result += key;
      }
    }
  }
  return result;
};
