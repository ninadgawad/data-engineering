## Spring JPA Best Practices
- Turn off `spring.jpa.open-in-view
- Call external services outside of database transaction
- Turn off auto-commit
- Be very careful with @Transactional(propagation = REQUIRES_NEW)
- Use TransactionTemplate when you need more control
- Avoid select on insert with @Version or implement Persistable
- Use Repository#getReferenceByld when you need ... references
- Always use FetchType.LAZY on @ManyToOne, @ManyToMany
- Explicitly fetch associations with fetch join or @EntityGraph
- Use @DynamicUpdate for table with large number of columns


## Reference
- https://maciejwalkowiak.com/
- https://www.baeldung.com/spring-flexypool-guide
- https://blogs.oracle.com/developers/post/hikaricp-best-practices-for-oracle-database-and-spring-boot
- https://vladmihalcea.com/books/high-performance-java-persistence/
- https://github.com/quick-perf/quickperf
