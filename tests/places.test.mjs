import test from 'node:test';
import assert from 'node:assert/strict';
import {coordinates,nearbyUrl,placeUrl,places,queryUrl} from '../web/model.mjs';
const config={providers:{wikimedia:'https://commons.wikimedia.org/w/api.php'}};
test('nearby requests only file namespace with licence and creator metadata',()=>{
 const u=new URL(queryUrl({mode:'nearby',lat:44.649,lon:-63.575,radius:1000},config));
 assert.equal(u.searchParams.get('generator'),'geosearch');assert.equal(u.searchParams.get('ggsnamespace'),'6');assert.equal(u.searchParams.get('ggscoord'),'44.649|-63.575');assert.match(u.searchParams.get('iiprop'),/extmetadata/);assert.equal(u.searchParams.get('ggslimit'),'50');
});
test('coordinates and radius reject blank, nonfinite and out-of-range values',()=>{
 for(const c of [['',0],[91,0],[0,-181],['foo',0]])assert.throws(()=>coordinates(...c));
 assert.deepEqual(coordinates(0,0),{lat:0,lon:0});
 for(const radius of [0,10001,1.5])assert.throws(()=>nearbyUrl({lat:1,lon:1,radius},config));
});
test('arbitrary place searches are encoded and matches require earth coordinates',()=>{
 const u=new URL(placeUrl('Lunenburg & district'));assert.equal(u.searchParams.get('gsrsearch'),'Lunenburg & district');
 assert.deepEqual(places({query:{pages:{a:{title:'Mars',coordinates:[{globe:'mars',lat:1,lon:2}]},b:{title:'Town',index:2,coordinates:[{globe:'earth',lat:3,lon:4}]},c:{title:'Missing'}}}}),[{title:'Town',lat:3,lon:4}]);
});
