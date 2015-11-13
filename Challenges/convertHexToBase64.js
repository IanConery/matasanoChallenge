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

var base64Array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/'];

var binaryToBase64 = function(array){
  var result = 0;
  var values = [32, 16, 8, 4, 2, 1];
  for(var i = 0; i < array.length; i++){
    if(array[i] === '1'){
      result += values[i];
    }
  }
  return result;
};

var convert = function(string){
  var binaryString = '';
  var base64Index = [];
  var base64Char = '';
  for(var i = 0; i < string.length; i++){
    binaryString += hexHash[string[i]];
  }
  binaryString = binaryString.split('');
  while(binaryString.length >= 6){
    var temp = binaryString.splice(0,6);
    base64Index.push(binaryToBase64(temp));
  }
  for(var i = 0; i < base64Index.length; i++){
    base64Char += base64Array[base64Index[i]];
  }

  if(binaryString.length > 0){
    var temp = binaryString.join('');
    while(temp.length < 7){
      temp += '0';
    }
    base64Char += base64Array[binaryToBase64(temp)];
    if(binaryString.length === 2){
      base64Char += '==';
    }else{
      base64Char += '==';
    }
  }

  return base64Char;
};
