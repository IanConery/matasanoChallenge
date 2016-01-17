//This assumes that each 'block' that is passed to this function is hex incodeded and in string form
//this function will check each block to ensure that it contains 16 bytes of data, if it doesn't then the function will add \x04 bytes until the length equals 16 bytes
var pkcsPadding = function(block){
  var length = block.length / 2;

  while(length < 16){
    block += '04';
    length ++;
  }
  return block;
};

console.log(pkcsPadding('a3bb0597'));