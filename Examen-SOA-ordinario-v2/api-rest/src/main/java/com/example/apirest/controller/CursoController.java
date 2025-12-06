package com.example.apirest.controller;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;       // <-- IMPORTANTE
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.apirest.model.Curso;
import com.example.apirest.repository.CursoRepository;

@RestController
@RequestMapping("/api/cursos")
@CrossOrigin(origins = "*")    // <-- ESTO ARREGLA EL CORS
public class CursoController {

    @Autowired
    private CursoRepository repo;

    // CREATE
    @PostMapping
    public Curso create(@RequestBody Curso c){
        return repo.save(c);
    }

    // LIST / SEARCH
    @GetMapping
    public List<Curso> list(@RequestParam(value="q", required=false) String q){
        if(q == null || q.isBlank()) return repo.findAll();
        return repo.findByNombreContainingIgnoreCase(q);
    }

    // GET BY ID
    @GetMapping("/{id}")
    public ResponseEntity<Curso> getById(@PathVariable Long id){
        Optional<Curso> opt = repo.findById(id);
        return opt.map(ResponseEntity::ok)
                  .orElse(ResponseEntity.notFound().build());
    }

    // UPDATE
    @PutMapping("/{id}")
    public ResponseEntity<Curso> update(@PathVariable Long id, @RequestBody Curso c){
        Optional<Curso> opt = repo.findById(id);
        if(opt.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Curso ex = opt.get();
        ex.setNombre(c.getNombre());
        ex.setFechaInicio(c.getFechaInicio());
        ex.setDescripcion(c.getDescripcion());

        return ResponseEntity.ok(repo.save(ex));
    }

    // DELETE
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id){
        Optional<Curso> opt = repo.findById(id);
        if(opt.isEmpty()) return ResponseEntity.notFound().build();

        repo.delete(opt.get());
        return ResponseEntity.noContent().build();
    }
}
